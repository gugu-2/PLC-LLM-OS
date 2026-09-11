import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Next-Gen Commercial Aviation Titanium Electron Beam Additive Manufacturing (EBAM)**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., High-vacuum wire-feed thermionic emission electron gun vectoring, melt pool backscattered electron (BSE) topographic analysis, and layer-by-layer dynamic focus deflection). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Titanium_EBAM\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Next-Gen Commercial Aviation Titanium Electron Beam Additive Manufacturing (EBAM)

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_Titanium_EBAM_Controller
VAR_INPUT
    (* Essential Safety and System Enable *)
    bSystemEnable            : BOOL;     (* Main system enable interlock *)
    bEmergencyStop           : BOOL;     (* Hardware E-Stop OK (Normally Closed) *)
    bVacuumInterlockOk       : BOOL;     (* High vacuum chamber pressure < 10^-5 mBar *)
    bChamberDoorLocked       : BOOL;     (* Chamber physical door lock verification *)
    
    (* Process Variables - Electron Gun & Vectoring *)
    rBeamCurrentSetpt        : REAL;     (* Desired beam current in mA (0.0 to 50.0) *)
    rBeamVoltagekV           : REAL;     (* Actual accelerating voltage in kV *)
    rFocusCoilCurrent        : REAL;     (* Feedback from focus deflection coil in mA *)
    
    (* Process Variables - Melt Pool & Material *)
    rMeltPoolTempC           : REAL;     (* Melt pool pyrometer reading in Deg C *)
    rWireFeedRateMm_s        : REAL;     (* Titanium wire feed rate in mm/s *)
    rBSE_TopographySignal    : REAL;     (* Backscattered electron topography feedback (0-10V) *)
END_VAR
VAR_OUTPUT
    (* Status and Alarms *)
    bSystemReady             : BOOL;     (* Controller ready for emission *)
    bEmissionActive          : BOOL;     (* High voltage emission is active *)
    bSafetyFault             : BOOL;     (* Critical safety interlock lost *)
    bProcessWarning          : BOOL;     (* Non-critical process deviation warning *)
    
    (* Actuator Control Signals *)
    rGunBiasControlV         : REAL;     (* Grid bias control voltage for beam current *)
    rDeflectionX_mA          : REAL;     (* X-axis electromagnetic deflection control *)
    rDeflectionY_mA          : REAL;     (* Y-axis electromagnetic deflection control *)
    rFocusControl_mA         : REAL;     (* Dynamic focus coil control signal *)
END_VAR
VAR
    (* Internal State and Filtering *)
    iMachineState            : INT := 0; 
    iFaultCode               : INT := 0;
    
    (* Timers and Triggers *)
    tVacuumStabilize         : TON;
    tEmissionRamp            : TON;
    tCoolingTimer            : TON;
    
    (* PID Controllers (Simulated internal states for demonstration) *)
    rErrorBeamCurrent        : REAL := 0.0;
    rIntegralBeamCurrent     : REAL := 0.0;
    
    (* Filtering arrays and variables *)
    rTempFilterBuffer        : ARRAY[0..9] OF REAL;
    iFilterIndex             : INT := 0;
    rFilteredMeltPoolTemp    : REAL := 0.0;
    rTempSum                 : REAL := 0.0;
    i                        : INT;
END_VAR

(* === MAIN LOGIC: SAFETY INTERLOCKS === *)
IF NOT bEmergencyStop OR NOT bChamberDoorLocked THEN
    (* Immediate shutdown on critical safety loss *)
    bSafetyFault := TRUE;
    bSystemReady := FALSE;
    bEmissionActive := FALSE;
    rGunBiasControlV := -2000.0; (* Full cutoff bias *)
    rDeflectionX_mA := 0.0;
    rDeflectionY_mA := 0.0;
    rFocusControl_mA := 0.0;
    iMachineState := 99; (* FAULT STATE *)
    iFaultCode := 1; (* Safety Interlock Loss *)
    RETURN;
END_IF;

IF NOT bVacuumInterlockOk THEN
    (* Loss of vacuum requires safe beam termination *)
    bSafetyFault := TRUE;
    bEmissionActive := FALSE;
    rGunBiasControlV := -2000.0; 
    iMachineState := 99;
    iFaultCode := 2; (* Vacuum Loss *)
    RETURN;
END_IF;

(* === MAIN LOGIC: SENSOR FILTERING === *)
(* 10-sample moving average filter for Melt Pool Temperature Pyrometer *)
rTempSum := 0.0;
rTempFilterBuffer[iFilterIndex] := rMeltPoolTempC;
FOR i := 0 TO 9 DO
    rTempSum := rTempSum + rTempFilterBuffer[i];
END_FOR;
rFilteredMeltPoolTemp := rTempSum / 10.0;
iFilterIndex := (iFilterIndex + 1) MOD 10;

(* === MAIN LOGIC: STATE MACHINE === *)
CASE iMachineState OF
    0: (* SYSTEM STARTUP & CHECKS *)
        bSystemReady := FALSE;
        bSafetyFault := FALSE;
        bProcessWarning := FALSE;
        rGunBiasControlV := -2000.0; (* Ensure beam is off *)
        
        IF bSystemEnable THEN
            iMachineState := 10;
        END_IF;
        
    10: (* VACUUM STABILIZATION *)
        tVacuumStabilize(IN := TRUE, PT := T#10S);
        IF tVacuumStabilize.Q THEN
            tVacuumStabilize(IN := FALSE);
            bSystemReady := TRUE;
            iMachineState := 20;
        END_IF;
        
    20: (* READY TO EMIT *)
        IF rBeamCurrentSetpt > 0.1 AND rBeamVoltagekV > 55.0 THEN
            bSystemReady := FALSE;
            iMachineState := 30;
        END_IF;
        IF NOT bSystemEnable THEN
            iMachineState := 0;
        END_IF;
        
    30: (* EMISSION RAMP UP AND PID CONTROL *)
        bEmissionActive := TRUE;
        tEmissionRamp(IN := TRUE, PT := T#2S);
        
        (* PI Control for Beam Current via Grid Bias *)
        rErrorBeamCurrent := rBeamCurrentSetpt - (rGunBiasControlV * -0.025); (* Simulated feedback calc *)
        rIntegralBeamCurrent := rIntegralBeamCurrent + (rErrorBeamCurrent * 0.01);
        
        (* Anti-windup *)
        IF rIntegralBeamCurrent > 500.0 THEN rIntegralBeamCurrent := 500.0; END_IF;
        IF rIntegralBeamCurrent < -500.0 THEN rIntegralBeamCurrent := -500.0; END_IF;
        
        (* Control Output Calculation (-2000V to 0V typical range) *)
        rGunBiasControlV := -2000.0 + (rErrorBeamCurrent * 5.0) + (rIntegralBeamCurrent * 1.5);
        
        (* Limit control output *)
        IF rGunBiasControlV > 0.0 THEN rGunBiasControlV := 0.0; END_IF;
        IF rGunBiasControlV < -2000.0 THEN rGunBiasControlV := -2000.0; END_IF;
        
        (* Dynamic Focus based on BSE Topography and Melt Pool Temp *)
        rFocusControl_mA := 500.0 + (rBSE_TopographySignal * 10.0) - (rFilteredMeltPoolTemp * 0.05);
        
        IF rBeamCurrentSetpt <= 0.1 THEN
            tEmissionRamp(IN := FALSE);
            bEmissionActive := FALSE;
            rIntegralBeamCurrent := 0.0;
            iMachineState := 40;
        END_IF;
        
    40: (* COOLING AND BEAM OFF *)
        tCoolingTimer(IN := TRUE, PT := T#5S);
        rGunBiasControlV := -2000.0;
        rFocusControl_mA := 0.0;
        rDeflectionX_mA := 0.0;
        rDeflectionY_mA := 0.0;
        
        IF tCoolingTimer.Q THEN
            tCoolingTimer(IN := FALSE);
            iMachineState := 20;
        END_IF;
        
    99: (* FAULT STATE *)
        bEmissionActive := FALSE;
        rGunBiasControlV := -2000.0;
        IF NOT bEmergencyStop AND bChamberDoorLocked AND bVacuumInterlockOk AND NOT bSystemEnable THEN
            bSafetyFault := FALSE;
            iFaultCode := 0;
            iMachineState := 0;
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
