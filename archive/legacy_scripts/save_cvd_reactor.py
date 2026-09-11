import os
import json, uuid

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Semiconductor Chemical Vapor Deposition (CVD) Epitaxial Reactor**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Trichlorosilane (TCS) precursor mass flow dynamic mixing, RF induction coil susceptor thermal mapping, and hydrogen carrier gas laminar flow profiling). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_EpitaxialCVDReactor\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Semiconductor Chemical Vapor Deposition (CVD) Epitaxial Reactor

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_EpitaxialCVDReactor
VAR_INPUT
    (* Required: at least 4-8 physical inputs with types and comments *)
    bEnable                 : BOOL;     (* System enable and start process signal *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal - MUST BE TRUE TO OPERATE *)
    rSusceptorTemp_C        : REAL;     (* Multi-wavelength pyrometer reading of susceptor temperature [deg C] *)
    rChamberPressure_Torr   : REAL;     (* Baratron capacitance manometer reading [Torr] *)
    rTCS_FlowRate_sccm      : REAL;     (* Trichlorosilane (TCS) mass flow feedback [sccm] *)
    rH2_Carrier_Flow_slm    : REAL;     (* Hydrogen carrier gas flow feedback [slm] *)
    bRF_Generator_OK        : BOOL;     (* RF induction heater fault status (TRUE = Healthy) *)
END_VAR
VAR_OUTPUT
    (* Required: at least 3-6 outputs with types and comments *)
    bSystemReady            : BOOL;     (* System ready for recipe execution *)
    rRF_GeneratorPower_kW   : REAL;     (* Output power command to RF induction generator [kW] *)
    rThrottleValve_Pos_Pct  : REAL;     (* Output to butterfly throttle valve for pressure control [%] *)
    rTCS_MFC_Setpoint       : REAL;     (* Mass flow controller setpoint for TCS precursor [sccm] *)
    bAlarm                  : BOOL;     (* Critical fault alarm output to interlock matrix *)
    iActiveStep             : INT;      (* Current recipe execution step *)
END_VAR
VAR
    (* Internal state and memory variables *)
    iState                  : INT := 0;
    tStepTimer              : TON;
    rTempError              : REAL;
    rTempIntegral           : REAL;
    rTempDerivative         : REAL;
    rLastTempError          : REAL;
    
    (* PID Constants for Thermal Control *)
    Kp_Temp                 : REAL := 2.45;
    Ki_Temp                 : REAL := 0.12;
    Kd_Temp                 : REAL := 0.50;
    
    (* Recipe parameters *)
    rTargetDepTemp_C        : REAL := 1150.0; (* Silicon epitaxy typical temperature *)
    rTargetPressure_Torr    : REAL := 80.0;   (* Reduced pressure CVD setpoint *)
END_VAR

(* === MAIN LOGIC === *)
(* Global Safety Interlocks *)
IF NOT bEmergencyStop OR NOT bRF_Generator_OK THEN
    bSystemReady := FALSE;
    bAlarm := TRUE;
    rRF_GeneratorPower_kW := 0.0;
    rThrottleValve_Pos_Pct := 100.0; (* Fail open to evacuate chamber *)
    rTCS_MFC_Setpoint := 0.0;
    iState := 999; (* FAULT STATE *)
    RETURN;
END_IF;

CASE iState OF
    0: (* IDLE & INITIALIZATION *)
        bSystemReady := TRUE;
        bAlarm := FALSE;
        rRF_GeneratorPower_kW := 0.0;
        rTCS_MFC_Setpoint := 0.0;
        rThrottleValve_Pos_Pct := 100.0;
        iActiveStep := 0;
        
        IF bEnable THEN
            bSystemReady := FALSE;
            iState := 10;
        END_IF;

    10: (* H2 PURGE & PRESSURE STABILIZATION *)
        iActiveStep := 1;
        (* Close throttle valve slightly to build target pressure *)
        IF rChamberPressure_Torr < rTargetPressure_Torr THEN
            rThrottleValve_Pos_Pct := rThrottleValve_Pos_Pct - 0.5;
        ELSIF rChamberPressure_Torr > rTargetPressure_Torr + 5.0 THEN
            rThrottleValve_Pos_Pct := rThrottleValve_Pos_Pct + 0.5;
        END_IF;
        
        tStepTimer(IN := TRUE, PT := T#30S);
        IF tStepTimer.Q THEN
            tStepTimer(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* SUSCEPTOR HEAT-UP TO DEPOSITION TEMP *)
        iActiveStep := 2;
        
        (* Thermal PID Control *)
        rTempError := rTargetDepTemp_C - rSusceptorTemp_C;
        rTempIntegral := rTempIntegral + (rTempError * 0.1); (* Assuming 100ms cycle *)
        rTempDerivative := (rTempError - rLastTempError) / 0.1;
        
        rRF_GeneratorPower_kW := (Kp_Temp * rTempError) + (Ki_Temp * rTempIntegral) + (Kd_Temp * rTempDerivative);
        rLastTempError := rTempError;
        
        (* Clamp Output Power to safe limits *)
        IF rRF_GeneratorPower_kW > 150.0 THEN
            rRF_GeneratorPower_kW := 150.0;
        ELSIF rRF_GeneratorPower_kW < 0.0 THEN
            rRF_GeneratorPower_kW := 0.0;
        END_IF;
        
        IF ABS(rTempError) < 5.0 THEN
            tStepTimer(IN := TRUE, PT := T#60S); (* Thermal soak *)
            IF tStepTimer.Q THEN
                tStepTimer(IN := FALSE);
                iState := 30;
            END_IF;
        ELSE
            tStepTimer(IN := FALSE);
        END_IF;

    30: (* PRECURSOR DEPOSITION (TCS INJECTION) *)
        iActiveStep := 3;
        
        (* Maintain thermal control *)
        rTempError := rTargetDepTemp_C - rSusceptorTemp_C;
        rTempIntegral := rTempIntegral + (rTempError * 0.1);
        rRF_GeneratorPower_kW := (Kp_Temp * rTempError) + (Ki_Temp * rTempIntegral);
        
        (* Introduce Trichlorosilane (TCS) mass flow for epitaxial growth *)
        rTCS_MFC_Setpoint := 500.0; (* 500 sccm typical for 200mm wafer *)
        
        tStepTimer(IN := TRUE, PT := T#300S); (* 5 minutes deposition time *)
        IF tStepTimer.Q THEN
            tStepTimer(IN := FALSE);
            rTCS_MFC_Setpoint := 0.0;
            iState := 40;
        END_IF;

    40: (* COOL-DOWN AND PURGE *)
        iActiveStep := 4;
        rRF_GeneratorPower_kW := 0.0; (* Turn off induction coil *)
        rTCS_MFC_Setpoint := 0.0;
        rThrottleValve_Pos_Pct := 100.0; (* Open valve *)
        
        IF rSusceptorTemp_C < 200.0 THEN
            iState := 50;
        END_IF;

    50: (* RECIPE COMPLETE *)
        iActiveStep := 5;
        bSystemReady := TRUE;
        IF NOT bEnable THEN
            iState := 0;
        END_IF;
        
    999: (* FAULT HANDLING *)
        bAlarm := TRUE;
        rRF_GeneratorPower_kW := 0.0;
        rTCS_MFC_Setpoint := 0.0;
        IF NOT bEmergencyStop THEN
            (* Wait for operator reset *)
            iState := 999;
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print("File saved successfully.")
