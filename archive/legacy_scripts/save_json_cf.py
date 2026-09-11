import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Commercial Aircraft Carbon Fiber Tape Laying Machine (ATL)**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 11-axis kinematic robotic head positioning, thermoplastic laser consolidation heating control, and dynamic ply tensioning on double-curvature molds). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_CarbonFiberATL\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Commercial Aircraft Carbon Fiber Tape Laying Machine (ATL)

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_CarbonFiberATL
VAR_INPUT
    (* Required: at least 4-8 physical inputs with types and comments *)
    bEnable                 : BOOL;     (* System enable signal *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal *)
    rLaserTempSetPt         : REAL;     (* Laser consolidation temperature setpoint [degC] *)
    rActualTemp             : REAL;     (* Pyrometer temperature feedback [degC] *)
    rTensionSetPt           : REAL;     (* Tape tension setpoint [N] *)
    rActualTension          : REAL;     (* Load cell tension feedback [N] *)
    rLayingSpeed            : REAL;     (* Tape laying velocity [m/s] *)
    rMouldCurvature         : REAL;     (* Local curvature radius of the mould [mm] *)
END_VAR
VAR_OUTPUT
    (* Required: at least 3-6 outputs with types and comments *)
    bSystemReady            : BOOL;     (* System ready status *)
    rLaserPowerCmd          : REAL;     (* Output to laser power controller [0-100%] *)
    rTensionTorqueCmd       : REAL;     (* Output torque command to payoff spool [Nm] *)
    rCompactionForceCmd     : REAL;     (* Pneumatic cylinder pressure command [bar] *)
    bAlarm                  : BOOL;     (* Fault alarm output *)
    iErrorCode              : INT;      (* Diagnostics error code *)
END_VAR
VAR
    (* Internal state variables *)
    iState                  : INT := 0;
    tTimer                  : TON;
    tHeatingStableTimer     : TON;
    
    (* PID internal variables for Laser Heating *)
    rTempError              : REAL;
    rTempIntegral           : REAL;
    rTempDerivative         : REAL;
    rTempLastError          : REAL;
    rKp_Heat                : REAL := 2.5;
    rKi_Heat                : REAL := 0.1;
    rKd_Heat                : REAL := 0.05;
    
    (* PID internal variables for Tension Control *)
    rTensionError           : REAL;
    rTensionIntegral        : REAL;
    rTensionLastError       : REAL;
    rKp_Tension             : REAL := 1.2;
    rKi_Tension             : REAL := 0.8;
    
    (* Feedforward variables *)
    rFF_Power               : REAL;
    rFF_Torque              : REAL;
END_VAR

(* === MAIN LOGIC === *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bAlarm := TRUE;
    iErrorCode := 9999;
    rLaserPowerCmd := 0.0;
    rTensionTorqueCmd := 0.0;
    rCompactionForceCmd := 0.0;
    iState := 0;
    RETURN;
END_IF;

CASE iState OF
    0: (* IDLE *)
        bSystemReady := FALSE;
        bAlarm := FALSE;
        iErrorCode := 0;
        rLaserPowerCmd := 0.0;
        rTensionTorqueCmd := 0.0;
        rCompactionForceCmd := 0.0;
        
        IF bEnable THEN
            (* Initialize PID variables *)
            rTempIntegral := 0.0;
            rTempLastError := 0.0;
            rTensionIntegral := 0.0;
            rTensionLastError := 0.0;
            iState := 10;
        END_IF;

    10: (* WARM-UP & PRE-TENSION *)
        (* Heating Control *)
        rTempError := rLaserTempSetPt - rActualTemp;
        rTempIntegral := rTempIntegral + rTempError;
        rLaserPowerCmd := (rKp_Heat * rTempError) + (rKi_Heat * rTempIntegral);
        IF rLaserPowerCmd > 100.0 THEN rLaserPowerCmd := 100.0; END_IF;
        IF rLaserPowerCmd < 0.0 THEN rLaserPowerCmd := 0.0; END_IF;
        
        (* Tension Control *)
        rTensionError := rTensionSetPt - rActualTension;
        rTensionIntegral := rTensionIntegral + rTensionError;
        rTensionTorqueCmd := (rKp_Tension * rTensionError) + (rKi_Tension * rTensionIntegral);
        
        tHeatingStableTimer(IN := (ABS(rTempError) < 5.0 AND ABS(rTensionError) < 2.0), PT := T#3S);
        
        IF tHeatingStableTimer.Q THEN
            tHeatingStableTimer(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* DYNAMIC LAYING *)
        bSystemReady := TRUE;
        
        (* Advanced Feedforward Heating Control based on laying speed and mould curvature *)
        rFF_Power := rLayingSpeed * 15.0 + (1000.0 / (rMouldCurvature + 1.0));
        rTempError := rLaserTempSetPt - rActualTemp;
        rTempIntegral := rTempIntegral + rTempError;
        rTempDerivative := rTempError - rTempLastError;
        rLaserPowerCmd := rFF_Power + (rKp_Heat * rTempError) + (rKi_Heat * rTempIntegral) + (rKd_Heat * rTempDerivative);
        rTempLastError := rTempError;
        
        IF rLaserPowerCmd > 100.0 THEN rLaserPowerCmd := 100.0; END_IF;
        IF rLaserPowerCmd < 0.0 THEN rLaserPowerCmd := 0.0; END_IF;
        
        (* Tension and Compaction force adjustments for double-curvature geometry *)
        rTensionError := rTensionSetPt - rActualTension;
        rTensionIntegral := rTensionIntegral + rTensionError;
        rFF_Torque := rLayingSpeed * 0.5;
        rTensionTorqueCmd := rFF_Torque + (rKp_Tension * rTensionError) + (rKi_Tension * rTensionIntegral);
        
        (* Modulate compaction force based on curvature to prevent fiber wrinkling *)
        IF rMouldCurvature < 500.0 THEN
            rCompactionForceCmd := 6.0; (* High pressure for tight curves *)
        ELSE
            rCompactionForceCmd := 4.5; (* Standard pressure for flat regions *)
        END_IF;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;
        
        (* Fault Detection *)
        IF ABS(rTempError) > 20.0 THEN
            bAlarm := TRUE;
            iErrorCode := 1001; (* Thermal runaway or laser fail *)
            iState := 99;
        END_IF;
        
        IF ABS(rTensionError) > 15.0 THEN
            bAlarm := TRUE;
            iErrorCode := 1002; (* Tape breakage or jam *)
            iState := 99;
        END_IF;

    99: (* FAULT STATE *)
        bSystemReady := FALSE;
        rLaserPowerCmd := 0.0;
        rTensionTorqueCmd := 0.0;
        rCompactionForceCmd := 0.0;
        IF NOT bEnable AND NOT bEmergencyStop THEN
            iState := 0; (* Reset only if user disables and estop is pressed/released appropriately *)
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
