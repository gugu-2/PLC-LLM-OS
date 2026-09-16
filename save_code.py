import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial Scale Lithium-Ion Battery Slurry Mixing Viscosity Regulation**

Task: Invent a highly complex, ultra-realistic control scenario for this domain. Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_LiIon_BatterySlurryMixing\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
   record = {\"messages\": [{\"role\": \"user\", \"content\": prompt}, {\"role\": \"assistant\", \"content\": code}]}
   with open(f\"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json\", \"w\", encoding=\"utf-8\") as f:
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Scale Lithium-Ion Battery Slurry Mixing Viscosity Regulation

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_LiIon_BatterySlurryMixing
VAR_INPUT
    bEnable                 : BOOL;     (* Main system enable command *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal (E-Stop) *)
    bDriveHealthy           : BOOL;     (* VFD healthy status signal *)
    rMeasuredViscosity      : REAL;     (* Current slurry viscosity in mPa.s *)
    rTempProcess            : REAL;     (* Process temperature in deg C *)
    rAgitatorSpeedFbk       : REAL;     (* Actual agitator speed in RPM *)
    rViscositySetpoint      : REAL;     (* Target viscosity in mPa.s *)
    bCleanInPlace           : BOOL;     (* CIP mode activation *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* Ready for production *)
    bRunning                : BOOL;     (* Mixer is currently running *)
    rAgitatorSpeedRef       : REAL;     (* Speed reference to VFD in RPM *)
    rSolventDosageValve     : REAL;     (* Output to NMP solvent dosing valve (0-100%) *)
    bAlarm                  : BOOL;     (* Critical fault alarm *)
    bWarning                : BOOL;     (* Process warning (e.g., viscosity deviation) *)
END_VAR
VAR
    iState                  : INT := 0; (* Internal state machine *)
    tTimer                  : TON;      (* State transition timer *)
    tViscosityFilter        : TON;      (* Measurement stability timer *)
    rViscosityError         : REAL;     (* Viscosity deviation from setpoint *)
    rIntegralSum            : REAL;     (* PID integral term for viscosity control *)
    bInterlockTriggered     : BOOL;     (* Internal interlock flag *)
    
    (* Filter variables *)
    rViscosityFiltered      : REAL;
    rAlpha                  : REAL := 0.1; (* Low pass filter coefficient *)
    
    (* Safety limits *)
    rMaxTemp                : REAL := 65.0; (* Max allowable temp *)
    rMinAgitatorSpeed       : REAL := 10.0; (* Min speed to prevent settling *)
END_VAR

(* === MAIN LOGIC === *)

(* 1. Safety Interlocks & Emergency Stop *)
IF NOT bEmergencyStop OR NOT bDriveHealthy OR rTempProcess > rMaxTemp THEN
    bInterlockTriggered := TRUE;
    bSystemReady := FALSE;
    bRunning := FALSE;
    rAgitatorSpeedRef := 0.0;
    rSolventDosageValve := 0.0;
    bAlarm := TRUE;
    iState := 99; (* Fault state *)
    RETURN;
ELSE
    bInterlockTriggered := FALSE;
    bAlarm := FALSE;
END_IF;

(* 2. Sensor Noise Filtering (Exponential Moving Average) *)
rViscosityFiltered := (rAlpha * rMeasuredViscosity) + ((1.0 - rAlpha) * rViscosityFiltered);

(* 3. Viscosity Error Calculation *)
rViscosityError := rViscosityFiltered - rViscositySetpoint;
IF ABS(rViscosityError) > 500.0 THEN
    bWarning := TRUE;
ELSE
    bWarning := FALSE;
END_IF;

(* 4. State Machine Control *)
CASE iState OF
    0: (* IDLE *)
        bSystemReady := TRUE;
        bRunning := FALSE;
        rAgitatorSpeedRef := 0.0;
        rSolventDosageValve := 0.0;
        
        IF bEnable AND NOT bInterlockTriggered THEN
            iState := 10;
        END_IF;

    10: (* PRE-MIX STARTUP *)
        bSystemReady := FALSE;
        bRunning := TRUE;
        (* Ramp up agitator speed safely *)
        rAgitatorSpeedRef := rMinAgitatorSpeed * 2.0;
        
        tTimer(IN := TRUE, PT := T#15S);
        IF tTimer.Q AND rAgitatorSpeedFbk > rMinAgitatorSpeed THEN
            tTimer(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* ACTIVE MIXING AND VISCOSITY REGULATION *)
        bRunning := TRUE;
        
        (* PI Control for Solvent Dosing based on Viscosity *)
        IF rViscosityError > 0.0 THEN
            (* Viscosity too high - add solvent *)
            rIntegralSum := rIntegralSum + (rViscosityError * 0.01);
            IF rIntegralSum > 100.0 THEN rIntegralSum := 100.0; END_IF; (* Anti-windup *)
            
            rSolventDosageValve := (rViscosityError * 0.05) + rIntegralSum;
            
            (* Limit valve output *)
            IF rSolventDosageValve > 100.0 THEN rSolventDosageValve := 100.0; END_IF;
        ELSE
            (* Viscosity low or at setpoint - stop solvent *)
            rSolventDosageValve := 0.0;
            rIntegralSum := 0.0;
        END_IF;
        
        (* Maintain optimal agitator speed *)
        rAgitatorSpeedRef := 300.0; (* 300 RPM optimal mixing speed *)
        
        IF NOT bEnable THEN
            rSolventDosageValve := 0.0;
            iState := 30;
        END_IF;

    30: (* RAMP DOWN AND STOP *)
        bRunning := FALSE;
        rSolventDosageValve := 0.0;
        rAgitatorSpeedRef := rMinAgitatorSpeed;
        
        tTimer(IN := TRUE, PT := T#10S);
        IF tTimer.Q THEN
            tTimer(IN := FALSE);
            rAgitatorSpeedRef := 0.0;
            iState := 0;
        END_IF;
        
    99: (* FAULT HANDLING *)
        bSystemReady := FALSE;
        bRunning := FALSE;
        rAgitatorSpeedRef := 0.0;
        rSolventDosageValve := 0.0;
        
        IF bEmergencyStop AND bDriveHealthy AND rTempProcess <= (rMaxTemp - 5.0) AND NOT bEnable THEN
            (* Fault cleared and enable signal removed *)
            iState := 0;
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump({"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}, f, ensure_ascii=False)
