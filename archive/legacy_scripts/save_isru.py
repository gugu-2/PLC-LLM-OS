import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Advanced Spacecraft Mars In-Situ Resource Utilization (ISRU) Sabatier Reactor**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Martian CO2 cryogenic desublimation extraction, catalytic methanation thermal runaway cascading, and deep space liquid oxygen (LOX) zero-boil-off cryocooling). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_ISRU_SabatierReactor\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Advanced Spacecraft Mars In-Situ Resource Utilization (ISRU) Sabatier Reactor

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.
</USER_REQUEST>"""

code = """```iec-st
FUNCTION_BLOCK FB_ISRU_SabatierReactor
VAR_INPUT
    (* System Operation & Safety Master Control Signals *)
    bEnable             : BOOL;     (* System master enable signal for methanation process *)
    bEmergencyStop      : BOOL;     (* Critical safety interlock OK signal - Active HIGH means safe *)
    
    (* In-Situ Resource Sensing - Mars Environment & Reactants *)
    rCO2_AtmPressure    : REAL;     (* Martian atmospheric CO2 collection pressure in mbar *)
    rH2_MassFlowRate    : REAL;     (* H2 feedstock mass flow rate in g/s from electrolysis *)
    
    (* Thermal Diagnostics & Methanation Cascade Prevention *)
    rReactorCoreTemp    : REAL;     (* Methanation catalytic reactor core temperature (Kelvin) *)
    rLOX_TankTemp       : REAL;     (* Liquid Oxygen storage tank cryo-temperature (Kelvin) *)
END_VAR
VAR_OUTPUT
    (* System Status Flags *)
    bSystemReady        : BOOL;     (* Sabatier system reached nominal thermal states and is ready *)
    
    (* Active Actuation & Cryocooling Commands *)
    rReactorCoolantCmd  : REAL;     (* PWM output command for thermal management system (0-100%) *)
    rCryoCoolerPwrCmd   : REAL;     (* Cryocooler compressor power command for LOX zero-boil-off *)
    
    (* Cascade Alarms & Critical Failure Warnings *)
    bThermalRunawayAlarm: BOOL;     (* Critical thermal runaway cascading fault detected in reactor *)
    bBoilOffWarning     : BOOL;     (* LOX boil-off margin degradation warning - impending vaporization *)
END_VAR
VAR
    (* Internal state tracking and dynamic integrators *)
    iState              : INT := 0; (* Main deterministic state machine state index *)
    tSafetyTimer        : TON;      (* Process stabilization sequence timer *)
    tRunawayIntegrator  : TON;      (* Integration timer for exothermic runaway confirmation *)
    
    (* PID Thermal Controller Internal States *)
    rTempError          : REAL;
    rKp                 : REAL := 3.1415; (* Proportional gain for exothermic thermal loop *)
    rKi                 : REAL := 0.2718; (* Integral gain for exothermic thermal loop *)
    rIntegralTerm       : REAL := 0.0;
    
    (* Physical Limits & Setpoints *)
    rMaxCoolantCmd      : REAL := 100.0;  (* 100% duty cycle for active cooling pump *)
    rNominalReactionTemp: REAL := 673.15; (* 400C in Kelvin - Optimal Sabatier efficiency *)
    rMaxSafeTemp        : REAL := 750.0;  (* Critical safety threshold before catalyst degradation *)
    rZBOTargetTemp      : REAL := 90.188; (* Boiling point of Oxygen at 1 atm (Kelvin) *)
END_VAR

(* === ADVANCED METHANATION CONTROL LOGIC === *)

(* Primary Safety Interlock - Immediate Safing Procedure *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    rReactorCoolantCmd := 100.0; (* Full cooling activated to immediately arrest methanation reaction *)
    rCryoCoolerPwrCmd := 100.0;  (* Fail-safe maximum cryo effort to prevent LOX tank overpressure *)
    bThermalRunawayAlarm := (rReactorCoreTemp > rMaxSafeTemp);
    iState := 99; (* FORCE TO FAULT LATCH STATE *)
    RETURN;
END_IF;

(* Deep Space Zero Boil-Off (ZBO) LOX Cryocooler Control Loop *)
(* Non-linear proactive cooling based on temperature margin degradation *)
IF rLOX_TankTemp > (rZBOTargetTemp - 2.5) THEN
    rCryoCoolerPwrCmd := LIMIT(0.0, rCryoCoolerPwrCmd + 8.5, 100.0);
    bBoilOffWarning := TRUE;
ELSE
    rCryoCoolerPwrCmd := LIMIT(0.0, rCryoCoolerPwrCmd - 0.75, 100.0);
    bBoilOffWarning := FALSE;
END_IF;

(* Deterministic State Machine for Sabatier Processing *)
CASE iState OF
    0: (* IDLE & PRE-FLIGHT ATMOSPHERIC CHECK *)
        bSystemReady := FALSE;
        rReactorCoolantCmd := 0.0;
        bThermalRunawayAlarm := FALSE;
        (* Typical Mars atmospheric pressure is ~6.1 mbar. Ensure intake compressors are primed *)
        IF bEnable AND (rCO2_AtmPressure > 5.5) THEN 
            iState := 10;
        END_IF;

    10: (* PRE-HEATING & DESUBLIMATION PREP *)
        (* Waiting for reactor to reach exothermic self-sustaining threshold *)
        IF rReactorCoreTemp >= (rNominalReactionTemp - 50.0) THEN
            tSafetyTimer(IN := TRUE, PT := T#10S);
            IF tSafetyTimer.Q THEN
                tSafetyTimer(IN := FALSE);
                iState := 20;
            END_IF;
        ELSE
            tSafetyTimer(IN := FALSE, PT := T#10S);
        END_IF;

    20: (* ACTIVE METHANATION PHASE & EXOTHERMIC REGULATION *)
        bSystemReady := TRUE;
        rTempError := rReactorCoreTemp - rNominalReactionTemp;
        
        (* PI Controller for Highly Exothermic Reactor Thermal Management *)
        rIntegralTerm := rIntegralTerm + (rTempError * rKi * 0.1); (* 100ms cycle presumed *)
        rIntegralTerm := LIMIT(0.0, rIntegralTerm, rMaxCoolantCmd);
        
        rReactorCoolantCmd := LIMIT(0.0, (rKp * rTempError) + rIntegralTerm, rMaxCoolantCmd);
        
        (* Catalytic Thermal Runaway Cascade Detection and Prevention *)
        IF rReactorCoreTemp > rMaxSafeTemp THEN
            tRunawayIntegrator(IN := TRUE, PT := T#1500MS);
            IF tRunawayIntegrator.Q THEN
                bThermalRunawayAlarm := TRUE;
                iState := 99; (* Abort immediately to FAULT handling *)
            END_IF;
        ELSE
            tRunawayIntegrator(IN := FALSE, PT := T#1500MS);
        END_IF;
        
        (* Normal shutdown command received *)
        IF NOT bEnable THEN
            iState := 30; 
        END_IF;
        
    30: (* CONTROLLED COOLDOWN SEQUENCING *)
        bSystemReady := FALSE;
        rReactorCoolantCmd := 65.0; (* Sustained heavy cooling post-reaction to scrub residual heat *)
        (* Waiting for reactor core to become completely inert *)
        IF rReactorCoreTemp < 350.0 THEN
            iState := 0;
        END_IF;
        
    99: (* CRITICAL FAULT HANDLING & SAFING LATCH *)
        bSystemReady := FALSE;
        rReactorCoolantCmd := 100.0; (* Maximum capacity cooling engaged *)
        rIntegralTerm := 0.0;
        (* Manual intervention required: fault cleared only when core cools and master enable cycled *)
        IF (NOT bEnable) AND (rReactorCoreTemp < 350.0) THEN
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
