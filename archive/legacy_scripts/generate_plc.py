import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Advanced Hypersonic Scramjet Combustor Fuel Injection**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Supercritical endothermic hydrocarbon pyrolysis, shock-wave boundary layer interaction (SWBLI) mapping, and variable throat geometry dynamic throttling). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Scramjet_FuelInjection\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Advanced Hypersonic Scramjet Combustor Fuel Injection

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_Scramjet_FuelInjection_AdvancedControl
VAR_INPUT
    bEnableSys      : BOOL;     (* System master enable signal, required for active injection *)
    bEmergencyStop  : BOOL;     (* Safety interlock from flight termination system / FADEC, FALSE = trip *)
    rMachNumber     : REAL;     (* Freestream Mach number calculated from air data boom *)
    rDynamicPress   : REAL;     (* Dynamic pressure in combustor inlet (kPa) *)
    rCombustorTemp  : REAL;     (* Internal combustor wall temperature (Deg K) *)
    rFuelMassFlow   : REAL;     (* Current measured endothermic hydrocarbon fuel flow (kg/s) *)
    rShockPosSensor : REAL;     (* Distance of SWBLI separation point from inlet throat (mm) *)
END_VAR
VAR_OUTPUT
    bSystemReady    : BOOL;     (* True when startup sequence and thermal conditioning complete *)
    rPrimaryThrottle: REAL;     (* Commanded position for primary supercritical fuel throttling valve (0.0-100.0%) *)
    rPilotIgnition  : REAL;     (* Variable plasma torch duty cycle for sustained ignition (0.0-100.0%) *)
    rThroatGeoVane  : REAL;     (* Deflection command for variable geometry strut to trim shock position (deg) *)
    bFlameoutAlarm  : BOOL;     (* Critical alarm indicating loss of sustained combustion *)
    bThermOverload  : BOOL;     (* Critical alarm indicating imminent structural failure due to temp *)
END_VAR
VAR
    iState                  : INT := 0; (* Internal state machine tracker *)
    tIgnitionTimer          : TON;      (* Timer for ignition sequencing *)
    tFlameoutWatchdog       : TON;      (* Timer to detect prolonged absence of expected pressure rise *)
    rTargetEquivalenceRatio : REAL;     (* Calculated phi based on Mach and pressure *)
    rFilteredMach           : REAL;     (* First-order filtered Mach number to reject noise *)
    rFilteredPress          : REAL;     (* First-order filtered pressure *)
    rPrevMach               : REAL := 0.0;
    rShockPosError          : REAL;     (* Error between desired and actual shock position *)
    rShockPosInt            : REAL := 0.0;
    bInitializeDone         : BOOL := FALSE;
END_VAR

(* === MAIN LOGIC === *)
(* Emergency and Interlock Processing *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bFlameoutAlarm := FALSE;
    bThermOverload := FALSE;
    rPrimaryThrottle := 0.0;
    rPilotIgnition := 0.0;
    rThroatGeoVane := 0.0;
    iState := 0;
    RETURN;
END_IF;

(* Input Filtering - 1st Order Low-Pass for sensor noise suppression in hypersonic environment *)
IF NOT bInitializeDone THEN
    rFilteredMach := rMachNumber;
    rFilteredPress := rDynamicPress;
    bInitializeDone := TRUE;
ELSE
    rFilteredMach := (rFilteredMach * 0.8) + (rMachNumber * 0.2);
    rFilteredPress := (rFilteredPress * 0.8) + (rDynamicPress * 0.2);
END_IF;

(* Thermal Protection Logic *)
IF rCombustorTemp > 3200.0 THEN
    bThermOverload := TRUE;
    (* Force aggressive fuel cutback for regenerative cooling protection *)
    rPrimaryThrottle := rPrimaryThrottle * 0.5;
ELSE
    bThermOverload := FALSE;
END_IF;

(* Shock Wave Boundary Layer Interaction (SWBLI) Control (PI Controller for Geometry) *)
(* Desired shock position moves downstream with increasing Mach *)
rShockPosError := (150.0 + (rFilteredMach - 5.0) * 25.0) - rShockPosSensor;
rShockPosInt := rShockPosInt + (rShockPosError * 0.01);
(* Anti-windup for throat geometry vane *)
IF rShockPosInt > 15.0 THEN
    rShockPosInt := 15.0;
ELSIF rShockPosInt < -5.0 THEN
    rShockPosInt := -5.0;
END_IF;
rThroatGeoVane := (rShockPosError * 0.2) + rShockPosInt;

(* Limit geometry actuation bounds *)
IF rThroatGeoVane > 20.0 THEN
    rThroatGeoVane := 20.0;
ELSIF rThroatGeoVane < -10.0 THEN
    rThroatGeoVane := -10.0;
END_IF;

(* State Machine for Scramjet Operation Sequence *)
CASE iState OF
    0: (* IDLE & SYSTEM CHECK *)
        bSystemReady := FALSE;
        rPrimaryThrottle := 0.0;
        rPilotIgnition := 0.0;
        IF bEnableSys AND (rFilteredMach >= 4.5) THEN
            (* Valid takeover conditions for dual-mode transition *)
            iState := 10;
        END_IF;
        
    10: (* COLD FLOW ESTABLISHMENT *)
        bSystemReady := TRUE;
        (* Initiate thermal conditioning of fuel using regenerative passages *)
        rPrimaryThrottle := 5.0; (* Pre-chill flow *)
        tIgnitionTimer(IN := TRUE, PT := T#500MS);
        IF tIgnitionTimer.Q THEN
            tIgnitionTimer(IN := FALSE);
            iState := 20;
        END_IF;
        
    20: (* PLASMA IGNITION SEQUENCE *)
        rPilotIgnition := 100.0; (* Full plasma torch output *)
        rPrimaryThrottle := 15.0; (* Ignition fuel schedule *)
        tIgnitionTimer(IN := TRUE, PT := T#1200MS);
        IF tIgnitionTimer.Q THEN
            tIgnitionTimer(IN := FALSE);
            iState := 30;
        END_IF;
        
    30: (* SUSTAINED RAM/SCRAMJET COMBUSTION *)
        rPilotIgnition := 20.0; (* Reduced plasma power to act as flame holder *)
        (* Calculate dynamic target equivalence ratio (Phi) *)
        IF rFilteredMach < 6.0 THEN
            rTargetEquivalenceRatio := 0.8;
        ELSIF rFilteredMach < 8.0 THEN
            rTargetEquivalenceRatio := 0.95;
        ELSE
            rTargetEquivalenceRatio := 1.1; (* Fuel-rich for thermal management *)
        END_IF;
        
        (* Simple proportional fuel scheduling based on dynamic pressure and Phi *)
        rPrimaryThrottle := (rFilteredPress * rTargetEquivalenceRatio) * 0.15;
        
        (* Flameout Detection Watchdog: if expected pressure falls anomalously *)
        IF rFilteredPress < (rTargetEquivalenceRatio * 100.0) THEN
            tFlameoutWatchdog(IN := TRUE, PT := T#250MS);
        ELSE
            tFlameoutWatchdog(IN := FALSE);
        END_IF;
        
        IF tFlameoutWatchdog.Q THEN
            bFlameoutAlarm := TRUE;
            iState := 40; (* Transition to fault/relight *)
        ELSE
            bFlameoutAlarm := FALSE;
        END_IF;
        
        (* Shutdown condition *)
        IF NOT bEnableSys THEN
            iState := 50;
        END_IF;
        
    40: (* FAULT HANDLING / RELIGHT ATTEMPT *)
        rPrimaryThrottle := 0.0;
        rPilotIgnition := 0.0;
        bSystemReady := FALSE;
        (* Optional: Wait for conditions to normalize before allowing restart *)
        IF NOT bEnableSys THEN
            iState := 0;
        END_IF;
        
    50: (* CONTROLLED SHUTDOWN *)
        bSystemReady := FALSE;
        rPrimaryThrottle := rPrimaryThrottle * 0.9; (* Ramp down *)
        IF rPrimaryThrottle < 1.0 THEN
            rPrimaryThrottle := 0.0;
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

os.makedirs("C:/Users/majip/Downloads/LLM REASEARCH/data/swarm_raw", exist_ok=True)
filename = f"C:/Users/majip/Downloads/LLM REASEARCH/data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
