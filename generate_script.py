import json, uuid
import os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial Automated Paint Mixing and Viscosity Control for Aerospace Manufacturing**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_AeroPaint_Mixing\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Automated Paint Mixing and Viscosity Control for Aerospace Manufacturing

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_AeroPaint_Mixing
VAR_INPUT
    (* Core Enable and Safety *)
    bSystemEnable       : BOOL;     (* Main system enable command *)
    bEStop_Ok           : BOOL;     (* Emergency stop circuit healthy (TRUE = OK) *)
    bViscometerReady    : BOOL;     (* Inline viscometer health status *)
    
    (* Process Measurements *)
    rTemp_DegC          : REAL;     (* Current paint temperature [°C] *)
    rViscosity_cP       : REAL;     (* Current viscosity [Centipoise] *)
    rFlowRate_LPM       : REAL;     (* Current solvent flow rate [L/min] *)
    rTankLevel_Pct      : REAL;     (* Paint tank level [%] *)
    
    (* Setpoints & Tolerances *)
    rTargetViscosity    : REAL;     (* Target viscosity [cP] for aerospace spec *)
    rViscosityTolerance : REAL;     (* Acceptable deviation [cP] *)
END_VAR
VAR_OUTPUT
    bSystemReady        : BOOL;     (* System ready for active control *)
    bSolventValveCmd    : BOOL;     (* Command to open solvent addition valve *)
    rAgitatorSpeed_Hz   : REAL;     (* Commanded VFD frequency for agitator [Hz] *)
    
    (* Alarms & Status *)
    bCriticalAlarm      : BOOL;     (* Critical fault (e-stop, sensor failure) *)
    bViscosityInSpec    : BOOL;     (* Viscosity is within aerospace tolerance *)
    rViscosityError     : REAL;     (* Current error [cP] *)
END_VAR
VAR
    (* Internal State Machine *)
    iMixingState        : INT := 0; 
    
    (* Timers & Filters *)
    tSolventPulse       : TON;
    tDwellTimer         : TON;
    tStartupDelay       : TON;
    
    (* Filtered values *)
    rFiltViscosity      : REAL;
    
    (* PID pseudo-vars for solvent dosing *)
    rProportional       : REAL;
    rIntegral           : REAL;
    rDerivative         : REAL;
    rLastError          : REAL;
END_VAR

(* === MAIN LOGIC === *)

(* Safety and Interlocks: Highest Priority *)
IF NOT bEStop_Ok OR NOT bViscometerReady THEN
    iMixingState := 99; (* Fault state *)
END_IF;

(* Viscosity Signal Filtering (First Order Low Pass) *)
rFiltViscosity := rFiltViscosity + 0.1 * (rViscosity_cP - rFiltViscosity);

(* Error Calculation *)
rViscosityError := rFiltViscosity - rTargetViscosity;

(* Tolerance Check *)
IF ABS(rViscosityError) <= rViscosityTolerance THEN
    bViscosityInSpec := TRUE;
ELSE
    bViscosityInSpec := FALSE;
END_IF;

CASE iMixingState OF
    0: (* IDLE *)
        bSystemReady := FALSE;
        bSolventValveCmd := FALSE;
        rAgitatorSpeed_Hz := 0.0;
        bCriticalAlarm := FALSE;
        
        IF bSystemEnable AND bEStop_Ok THEN
            iMixingState := 10;
        END_IF;

    10: (* STARTUP AGITATION *)
        (* Run agitator at low speed to homogenize before measuring *)
        bSystemReady := FALSE;
        rAgitatorSpeed_Hz := 15.0; 
        
        tStartupDelay(IN := TRUE, PT := T#30S);
        IF tStartupDelay.Q THEN
            tStartupDelay(IN := FALSE);
            iMixingState := 20;
        END_IF;

    20: (* ACTIVE CONTROL - VISCOSITY ADJUSTMENT *)
        bSystemReady := TRUE;
        
        (* Modulate agitator based on tank level to avoid splashing/foaming *)
        IF rTankLevel_Pct > 50.0 THEN
            rAgitatorSpeed_Hz := 45.0;
        ELSIF rTankLevel_Pct > 20.0 THEN
            rAgitatorSpeed_Hz := 30.0;
        ELSE
            rAgitatorSpeed_Hz := 15.0;
        END_IF;
        
        (* Solvent Dosing Logic - Pulse Width Modulation based on error *)
        IF rViscosityError > rViscosityTolerance THEN
            (* Viscosity too high -> add solvent *)
            tSolventPulse(IN := TRUE, PT := T#2S);
            bSolventValveCmd := TRUE;
            
            IF tSolventPulse.Q THEN
                bSolventValveCmd := FALSE;
                tSolventPulse(IN := FALSE);
                iMixingState := 30; (* Go to dwell to let it mix *)
            END_IF;
        ELSE
            bSolventValveCmd := FALSE;
            tSolventPulse(IN := FALSE);
        END_IF;
        
        IF NOT bSystemEnable THEN
            iMixingState := 0;
        END_IF;

    30: (* DWELL / MIXING DELAY *)
        bSolventValveCmd := FALSE;
        tDwellTimer(IN := TRUE, PT := T#15S);
        
        IF tDwellTimer.Q THEN
            tDwellTimer(IN := FALSE);
            iMixingState := 20; (* Return to active control *)
        END_IF;
        
        IF NOT bSystemEnable THEN
            iMixingState := 0;
        END_IF;

    99: (* FAULT STATE *)
        bSystemReady := FALSE;
        bSolventValveCmd := FALSE;
        rAgitatorSpeed_Hz := 0.0;
        bCriticalAlarm := TRUE;
        tStartupDelay(IN := FALSE);
        tSolventPulse(IN := FALSE);
        tDwellTimer(IN := FALSE);
        
        IF bEStop_Ok AND bViscometerReady AND NOT bSystemEnable THEN
            (* Require enable toggle to reset *)
            iMixingState := 0;
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
