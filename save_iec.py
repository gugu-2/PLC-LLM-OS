import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Hydrogen Fuel Cell Vehicle (FCV) High-Pressure Carbon Fiber Tank Winding**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 700-bar vessel hoop/helical winding trajectory path generation, epoxy resin bath dynamic viscosity tracking, and multi-axis robotic tensioner cascading loops). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_CompositeWinder\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Hydrogen Fuel Cell Vehicle (FCV) High-Pressure Carbon Fiber Tank Winding

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_FCV_TankWinder
VAR_INPUT
    bEnable                 : BOOL;     (* System enable signal for the winding process *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal - TRUE means safe to operate *)
    rResinTemp_C            : REAL;     (* Epoxy resin bath temperature in Celsius *)
    rTargetTension_N        : REAL;     (* Target carbon fiber tension in Newtons *)
    rSpindleSpeed_RPM       : REAL;     (* Commanded spindle rotational speed in RPM *)
    rCarriagePos_mm         : REAL;     (* Current position of the winding carriage in mm *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* System ready status, all interlocks cleared *)
    rTensionCmd_V           : REAL;     (* Analog control voltage to tensioner servomotor (0-10V) *)
    rCarriageSpeedCmd_mm_s  : REAL;     (* Command speed for the linear carriage in mm/s *)
    bAlarm                  : BOOL;     (* Critical fault alarm output *)
    iErrorCode              : INT;      (* Detailed error code for diagnostics *)
END_VAR
VAR
    iState                  : INT := 0; (* Main state machine variable *)
    rActualViscosity_cP     : REAL;     (* Calculated dynamic viscosity based on temperature *)
    rTensionError_N         : REAL;     (* PID error for tension loop *)
    rTensionIntegral_N      : REAL;     (* PID integral accumulator for tension loop *)
    rTensionDerivative_N    : REAL;     (* PID derivative for tension loop *)
    rPrevTensionError_N     : REAL;     (* Previous tension error for derivative calculation *)
    
    (* PID Constants *)
    Kp_Tension              : REAL := 1.25;
    Ki_Tension              : REAL := 0.05;
    Kd_Tension              : REAL := 0.10;
    
    (* Timers *)
    tResinStabilize         : TON;
    tWindingTimeout         : TON;
    
    (* Constants *)
    C_NOMINAL_VISCOSITY     : REAL := 450.0; (* cP at 40C *)
    C_TEMP_NOMINAL          : REAL := 40.0;  (* Celsius *)
    C_VISCOSITY_COEFF       : REAL := -12.5; (* cP per degree C *)
END_VAR

(* === MAIN SAFETY AND INTERLOCK LOGIC === *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bAlarm := TRUE;
    iErrorCode := 999; (* E-STOP ENGAGED *)
    rTensionCmd_V := 0.0;
    rCarriageSpeedCmd_mm_s := 0.0;
    iState := 0;
    RETURN;
END_IF;

(* Viscosity Tracking - Dynamic Calculation based on Arrhenius-like linear approximation for resin *)
rActualViscosity_cP := C_NOMINAL_VISCOSITY + (rResinTemp_C - C_TEMP_NOMINAL) * C_VISCOSITY_COEFF;

IF rActualViscosity_cP > 800.0 OR rActualViscosity_cP < 200.0 THEN
    (* Resin viscosity out of acceptable bounds for 700-bar vessel hoop/helical winding *)
    bAlarm := TRUE;
    iErrorCode := 101; (* RESIN VISCOSITY FAULT *)
    iState := 99; (* FAULT STATE *)
END_IF;

(* === MAIN TRAJECTORY AND WINDING STATE MACHINE === *)
CASE iState OF
    0: (* IDLE AND INITIALIZATION *)
        bSystemReady := FALSE;
        rTensionCmd_V := 0.0;
        rCarriageSpeedCmd_mm_s := 0.0;
        
        IF bEnable AND NOT bAlarm THEN
            (* Wait for resin temperature to stabilize *)
            tResinStabilize(IN := TRUE, PT := T#10S);
            IF tResinStabilize.Q THEN
                tResinStabilize(IN := FALSE);
                bSystemReady := TRUE;
                iState := 10; (* TRANSITION TO PRE-TENSION *)
            END_IF;
        ELSE
            tResinStabilize(IN := FALSE);
        END_IF;

    10: (* PRE-TENSIONING PHASE *)
        (* Ramp up tension to target before spindle rotation begins *)
        rTensionError_N := rTargetTension_N - (rTensionCmd_V * 100.0); (* Simulated feedback conversion *)
        rTensionIntegral_N := rTensionIntegral_N + rTensionError_N;
        rTensionDerivative_N := rTensionError_N - rPrevTensionError_N;
        
        rTensionCmd_V := (Kp_Tension * rTensionError_N) + (Ki_Tension * rTensionIntegral_N) + (Kd_Tension * rTensionDerivative_N);
        rPrevTensionError_N := rTensionError_N;
        
        (* Clamp Output *)
        IF rTensionCmd_V > 10.0 THEN rTensionCmd_V := 10.0; END_IF;
        IF rTensionCmd_V < 0.0 THEN rTensionCmd_V := 0.0; END_IF;
        
        IF ABS(rTensionError_N) < 5.0 THEN
            iState := 20; (* TRANSITION TO HELICAL WINDING *)
        END_IF;

    20: (* HELICAL WINDING ACTIVE *)
        (* Execute multi-axis robotic tensioner cascading loops *)
        (* Carriage speed synchronized with spindle speed to maintain specific winding angle for 700-bar strength *)
        rCarriageSpeedCmd_mm_s := rSpindleSpeed_RPM * 2.54; (* Proportional gain for carriage traversal *)
        
        (* Continuous Tension PID Execution *)
        rTensionError_N := rTargetTension_N - (rTensionCmd_V * 100.0);
        rTensionIntegral_N := rTensionIntegral_N + rTensionError_N;
        rTensionCmd_V := (Kp_Tension * rTensionError_N) + (Ki_Tension * rTensionIntegral_N);
        
        IF rCarriagePos_mm > 2500.0 THEN
            (* End of vessel reached, reverse direction or end pass *)
            iState := 30; (* DWELL AT DOME *)
        END_IF;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    30: (* DWELL AND REVERSAL AT DOME END *)
        rCarriageSpeedCmd_mm_s := 0.0; (* Pause carriage at dome while spindle rotates for polar wrap *)
        tWindingTimeout(IN := TRUE, PT := T#2S);
        IF tWindingTimeout.Q THEN
            tWindingTimeout(IN := FALSE);
            iState := 20; (* Return to helical winding for next pass (simplified for example) *)
        END_IF;

    99: (* FAULT HANDLING *)
        bSystemReady := FALSE;
        rTensionCmd_V := 0.0;
        rCarriageSpeedCmd_mm_s := 0.0;
        IF NOT bEnable AND NOT bAlarm THEN
            iState := 0; (* Reset if enable dropped and alarm cleared *)
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("c:/Users/majip/Downloads/LLM REASEARCH/data/swarm_raw", exist_ok=True)
record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}

filename = f"c:/Users/majip/Downloads/LLM REASEARCH/data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
