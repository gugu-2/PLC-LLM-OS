import json, uuid, os
os.makedirs("data/swarm_raw", exist_ok=True)
prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial Scale Bio-Synthetic Artificial Meat Scaffold Perfusion Bioreactor**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Fibroblast shear-stress minimization, 3D capillary nutrient mass-transfer modeling, and pulsatile oxygenation flow emulation). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_ArtificialMeat_Bioreactor\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Scale Bio-Synthetic Artificial Meat Scaffold Perfusion Bioreactor

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_ArtificialMeat_Bioreactor_PerfusionControl
(* 
   =============================================================================
   Lumina AI Cloud Swarm - Elite Synthetic Data Architect
   Industrial Scale Bio-Synthetic Artificial Meat Scaffold Perfusion Bioreactor
   =============================================================================
   Description:
   Advanced PID-based multi-variable control for a 3D scaffold perfusion bioreactor.
   Handles pulsatile flow emulation for capillary nutrient mass-transfer modeling,
   minimizes fibroblast shear stress, and provides redundant safety interlocking.
   =============================================================================
*)
VAR_INPUT
    bSystemEnable           : BOOL;     (* Main system enable signal *)
    bSafetyRelayOk          : BOOL;     (* Hardware safety relay OK signal *)
    rScaffoldPressureIn     : REAL;     (* Inlet pressure measurement (kPa) *)
    rScaffoldPressureOut    : REAL;     (* Outlet pressure measurement (kPa) *)
    rNutrientFlowRate       : REAL;     (* Flow rate measurement (L/min) *)
    rDissolvedOxygen        : REAL;     (* Dissolved oxygen concentration (mg/L) *)
    rPulsatileTargetFreq    : REAL;     (* Target frequency for pulsatile emulation (Hz) *)
    rMaxShearStressLimit    : REAL;     (* Maximum allowable shear stress (dynes/cm2) *)
END_VAR

VAR_OUTPUT
    bSystemReady            : BOOL;     (* Bioreactor system ready status *)
    rMainPumpControl        : REAL;     (* VFD control signal for main perfusion pump (0-100%) *)
    rOxygenValveControl     : REAL;     (* Proportional valve control for O2 sparging (0-100%) *)
    bShearStressWarning     : BOOL;     (* Warning: approaching shear stress limit *)
    bCriticalAlarm          : BOOL;     (* Critical fault alarm output *)
    iOperatingState         : INT;      (* Current operating state code *)
END_VAR

VAR
    (* Internal State and Timers *)
    tStartupDelay           : TON;
    tPulseGenerator         : TON;
    iState                  : INT := 0;
    
    (* Filtering and Math *)
    rFilteredFlowRate       : REAL := 0.0;
    rCalculatedShearStress  : REAL := 0.0;
    rDeltaPressure          : REAL := 0.0;
    rPulseAmplitude         : REAL := 0.0;
    bPulsePhase             : BOOL := FALSE;
    
    (* PID State *)
    rFlowError              : REAL := 0.0;
    rFlowIntegral           : REAL := 0.0;
    rKp                     : REAL := 2.5;
    rKi                     : REAL := 0.4;
    
    (* Constants *)
    rViscosity              : REAL := 0.0012; (* Media viscosity (Pa.s) *)
    rScaffoldPermeability   : REAL := 1.5E-9; (* m2 *)
END_VAR

(* === MAIN LOGIC === *)

(* 1. Safety Interlocks and Hardware Checks *)
IF NOT bSafetyRelayOk THEN
    bSystemReady := FALSE;
    bCriticalAlarm := TRUE;
    rMainPumpControl := 0.0;
    rOxygenValveControl := 0.0;
    iOperatingState := -1;
    RETURN;
END_IF;

(* 2. Sensor Filtering (Exponential Moving Average) *)
rFilteredFlowRate := rFilteredFlowRate * 0.9 + rNutrientFlowRate * 0.1;
rDeltaPressure := rScaffoldPressureIn - rScaffoldPressureOut;

(* 3. Biomechanical Modeling: Shear Stress Calculation *)
(* Simplified Hagen-Poiseuille derivative for complex porous media *)
IF rFilteredFlowRate > 0.0 THEN
    rCalculatedShearStress := (rDeltaPressure * rViscosity * 1000.0) / (rScaffoldPermeability * 1.0E12);
ELSE
    rCalculatedShearStress := 0.0;
END_IF;

IF rCalculatedShearStress > (rMaxShearStressLimit * 0.9) THEN
    bShearStressWarning := TRUE;
ELSE
    bShearStressWarning := FALSE;
END_IF;

IF rCalculatedShearStress > rMaxShearStressLimit THEN
    bCriticalAlarm := TRUE;
    (* Force state machine to safe shutdown *)
    iState := 99;
END_IF;

(* 4. State Machine Control *)
CASE iState OF
    0: (* IDLE *)
        bSystemReady := FALSE;
        rMainPumpControl := 0.0;
        rOxygenValveControl := 0.0;
        iOperatingState := 0;
        
        IF bSystemEnable AND NOT bCriticalAlarm THEN
            tStartupDelay(IN := FALSE);
            iState := 10;
        END_IF;

    10: (* INITIALIZATION & PRIMING *)
        iOperatingState := 10;
        tStartupDelay(IN := TRUE, PT := T#10S);
        
        (* Low flow prime *)
        rMainPumpControl := 15.0; 
        
        IF tStartupDelay.Q THEN
            tStartupDelay(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* NORMAL PERFUSION (PULSATILE) *)
        bSystemReady := TRUE;
        iOperatingState := 20;
        
        (* Pulsatile flow emulation using TON *)
        tPulseGenerator(IN := NOT tPulseGenerator.Q, PT := REAL_TO_TIME(1000.0 / rPulsatileTargetFreq));
        
        IF tPulseGenerator.Q THEN
            bPulsePhase := NOT bPulsePhase;
        END_IF;
        
        IF bPulsePhase THEN
            rPulseAmplitude := 15.0; (* 15% bump during systole emulation *)
        ELSE
            rPulseAmplitude := 0.0;  (* Diastole emulation *)
        END_IF;
        
        (* PI Control for base flow *)
        rFlowError := 50.0 - rFilteredFlowRate; (* Target base flow 50 L/min *)
        rFlowIntegral := rFlowIntegral + (rFlowError * 0.1); 
        
        (* Anti-windup *)
        IF rFlowIntegral > 100.0 THEN rFlowIntegral := 100.0; END_IF;
        IF rFlowIntegral < -100.0 THEN rFlowIntegral := -100.0; END_IF;
        
        rMainPumpControl := (rFlowError * rKp) + (rFlowIntegral * rKi) + rPulseAmplitude;
        
        (* Clamp Pump Output *)
        IF rMainPumpControl > 100.0 THEN rMainPumpControl := 100.0; END_IF;
        IF rMainPumpControl < 0.0 THEN rMainPumpControl := 0.0; END_IF;
        
        (* Oxygenation Control *)
        IF rDissolvedOxygen < 4.5 THEN
            rOxygenValveControl := 60.0;
        ELSIF rDissolvedOxygen > 6.0 THEN
            rOxygenValveControl := 10.0;
        ELSE
            rOxygenValveControl := 35.0;
        END_IF;

        IF NOT bSystemEnable THEN
            iState := 0;
        END_IF;
        
    99: (* FAULT SHUTDOWN *)
        iOperatingState := 99;
        rMainPumpControl := 0.0;
        rOxygenValveControl := 100.0; (* Flush O2 to maintain cell viability on stop *)
        bSystemReady := FALSE;
        
        IF NOT bSystemEnable AND NOT bCriticalAlarm THEN
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
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
