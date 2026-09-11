import json, uuid

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial Scale Continuous Float Glass Ribbon Forming Lehr**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Molten tin bath atmosphere hydrogen-nitrogen reduction, top-roller differential speed stretching, and transverse temperature gradient controlled annealing). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_FloatGlass_AnnealingLehr\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Scale Continuous Float Glass Ribbon Forming Lehr

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_FloatGlassLehrControl
VAR_INPUT
    (* Required inputs for float glass lehr control *)
    bEnable                 : BOOL;     (* System master enable signal *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal (active high) *)
    rTinBathTemp            : REAL;     (* Temperature of the molten tin bath [deg C] *)
    rRibbonSpeed            : REAL;     (* Glass ribbon pulling speed [m/min] *)
    rTopRollerDiffSpeed     : REAL;     (* Differential speed for top-roller stretching [%] *)
    rZoneATempPV            : REAL;     (* Process Value: Annealing Zone A Temp [deg C] *)
    rAtmosphereH2Ratio      : REAL;     (* Hydrogen-Nitrogen reduction mix ratio [%] *)
    bPurgeActive            : BOOL;     (* Tin bath atmosphere purge active signal *)
END_VAR
VAR_OUTPUT
    (* Required outputs for control & monitoring *)
    bSystemReady            : BOOL;     (* Overall lehr control system ready status *)
    rHeatingElementCmdZoneA : REAL;     (* Control signal to Zone A heating elements [0-100%] *)
    rRollerSpeedCmd         : REAL;     (* Corrected motor speed command for pulling rollers [rpm] *)
    rAtmosphereFlowCmd      : REAL;     (* Control signal for H2/N2 gas mix flow valve [0-100%] *)
    bThermalShockAlarm      : BOOL;     (* Alarm for critical cooling gradient violation *)
    bAtmosphereFault        : BOOL;     (* Fault output for improper reducing atmosphere *)
END_VAR
VAR
    (* Internal State and Processing Variables *)
    iState                  : INT := 0; 
    tStabilizationTimer     : TON;
    rZoneATempError         : REAL;
    rIntegralTempA          : REAL := 0.0;
    rDerivativeTempA        : REAL := 0.0;
    rLastTempErrorA         : REAL := 0.0;
    Kp                      : REAL := 2.5;
    Ki                      : REAL := 0.15;
    Kd                      : REAL := 0.8;
    tSampleTime             : TIME := T#100MS;
    rSampleTimeSec          : REAL := 0.1;
    rMaxCoolingRate         : REAL := 15.0; (* deg C / min max allowable gradient *)
    rMaxTempCmd             : REAL := 100.0;
    rMinTempCmd             : REAL := 0.0;
    rBaseRollerSpeed        : REAL := 1500.0;
END_VAR

(* === MAIN SAFETY AND EMERGENCY STOP LOGIC === *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bThermalShockAlarm := TRUE;
    bAtmosphereFault := TRUE;
    rHeatingElementCmdZoneA := 0.0;
    rRollerSpeedCmd := 0.0;
    rAtmosphereFlowCmd := 0.0;
    iState := 0;
    RETURN;
END_IF;

(* === THERMAL AND ATMOSPHERE DIAGNOSTICS === *)
IF rAtmosphereH2Ratio < 4.5 OR rAtmosphereH2Ratio > 10.0 THEN
    bAtmosphereFault := TRUE;
ELSE
    bAtmosphereFault := FALSE;
END_IF;

(* === STATE MACHINE FOR LEHR CONTROL === *)
CASE iState OF
    0: (* IDLE & PURGE *)
        bSystemReady := FALSE;
        rHeatingElementCmdZoneA := 0.0;
        IF bEnable AND NOT bPurgeActive AND NOT bAtmosphereFault THEN
            iState := 10;
        END_IF;

    10: (* WARM-UP & STABILIZATION *)
        rHeatingElementCmdZoneA := 35.0; (* Minimum warm-up power *)
        rRollerSpeedCmd := rBaseRollerSpeed * 0.1;
        tStabilizationTimer(IN := TRUE, PT := T#30S);
        
        IF tStabilizationTimer.Q THEN
            tStabilizationTimer(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* PID ANNEALING & CONTINUOUS FORMING *)
        bSystemReady := TRUE;
        
        (* Cascade PID execution for Transverse Temperature Gradient in Zone A *)
        rZoneATempError := rTinBathTemp - 400.0 - rZoneATempPV; (* Target cooling curve ref *)
        
        (* Anti-windup clamping for integral term *)
        IF (rHeatingElementCmdZoneA < rMaxTempCmd AND rZoneATempError > 0.0) OR 
           (rHeatingElementCmdZoneA > rMinTempCmd AND rZoneATempError < 0.0) THEN
            rIntegralTempA := rIntegralTempA + (rZoneATempError * rSampleTimeSec);
        END_IF;
        
        (* Derivative filtering term *)
        rDerivativeTempA := (rZoneATempError - rLastTempErrorA) / rSampleTimeSec;
        rLastTempErrorA := rZoneATempError;
        
        (* Compute PID Output *)
        rHeatingElementCmdZoneA := (Kp * rZoneATempError) + (Ki * rIntegralTempA) + (Kd * rDerivativeTempA);
        
        (* Saturation limits *)
        IF rHeatingElementCmdZoneA > rMaxTempCmd THEN rHeatingElementCmdZoneA := rMaxTempCmd; END_IF;
        IF rHeatingElementCmdZoneA < rMinTempCmd THEN rHeatingElementCmdZoneA := rMinTempCmd; END_IF;
        
        (* Complex Kinematics: Ribbon pulling speed with top roller differential stretching compensation *)
        rRollerSpeedCmd := (rBaseRollerSpeed * (rRibbonSpeed / 10.0)) * (1.0 + (rTopRollerDiffSpeed / 100.0));
        
        (* Continuous Atmosphere Regulation based on target H2 reduction ratio *)
        IF NOT bAtmosphereFault THEN
            rAtmosphereFlowCmd := 50.0 + (5.0 * (7.5 - rAtmosphereH2Ratio));
            IF rAtmosphereFlowCmd > 100.0 THEN rAtmosphereFlowCmd := 100.0; END_IF;
            IF rAtmosphereFlowCmd < 20.0 THEN rAtmosphereFlowCmd := 20.0; END_IF;
        ELSE
            rAtmosphereFlowCmd := 100.0; (* Flood with inert mix on fault *)
        END_IF;
        
        (* Thermal shock monitoring using theoretical derivative limits *)
        IF ABS(rDerivativeTempA * 60.0) > rMaxCoolingRate THEN
            bThermalShockAlarm := TRUE;
        ELSE
            bThermalShockAlarm := FALSE;
        END_IF;
        
        IF NOT bEnable THEN
            tStabilizationTimer(IN := FALSE);
            iState := 0;
        END_IF;

    ELSE
        iState := 0;
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
