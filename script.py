import os, json, uuid

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: High-Speed Magnetic Levitation (Maglev) Vacuum Tube Hyperloop**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 1200km/h aerodynamic choke point mitigation, active superconducting levitation null-flux mapping, and sub-millisecond linear synchronous motor (LSM) block switching). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_HyperloopMaglevControl\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: High-Speed Magnetic Levitation (Maglev) Vacuum Tube Hyperloop

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_HyperloopMaglevControl
VAR_INPUT
    bSystemEnable           : BOOL;     (* Main hyperloop drive and levitation enable *)
    bEmergencyStop          : BOOL;     (* Safety loop interlock signal (active HIGH = OK) *)
    rTubePressure           : REAL;     (* Current vacuum tube pressure in Pascals *)
    rPodVelocity            : REAL;     (* Instantaneous pod velocity in m/s *)
    rPodPosition            : REAL;     (* Absolute position in the tube in meters *)
    rLevitationGap_FL       : REAL;     (* Front-Left levitation gap in mm *)
    rLevitationGap_FR       : REAL;     (* Front-Right levitation gap in mm *)
    rLevitationGap_RL       : REAL;     (* Rear-Left levitation gap in mm *)
    rLevitationGap_RR       : REAL;     (* Rear-Right levitation gap in mm *)
    rSuperconductorTemp     : REAL;     (* Highest superconductor temperature in Kelvin *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* Drive and levitation systems nominal and ready *)
    bPropulsionActive       : BOOL;     (* LSM propulsion is currently active *)
    rRequestedThrust        : REAL;     (* Force command to LSM in Newtons *)
    rLevitationCurrent_FL   : REAL;     (* Active null-flux coil current FL in Amps *)
    rLevitationCurrent_FR   : REAL;     (* Active null-flux coil current FR in Amps *)
    rLevitationCurrent_RL   : REAL;     (* Active null-flux coil current RL in Amps *)
    rLevitationCurrent_RR   : REAL;     (* Active null-flux coil current RR in Amps *)
    bCriticalAlarm          : BOOL;     (* Critical fault requiring immediate pod braking *)
    iAlarmCode              : INT;      (* Diagnostics code for fault classification *)
END_VAR
VAR
    iStateMachine           : INT := 0;
    rTargetVelocity         : REAL := 333.33; (* Nominal cruise 1200 km/h in m/s *)
    rMaxTubePressure        : REAL := 100.0;  (* Max allowable tube pressure in Pa *)
    rMaxSuperTemp           : REAL := 77.0;   (* Liquid nitrogen boiling point K *)
    rNominalGap             : REAL := 15.0;   (* Target levitation gap in mm *)
    rKp_Gap                 : REAL := 50.0;
    rKd_Gap                 : REAL := 10.0;
    rPrevGap_FL             : REAL := 15.0;
    rPrevGap_FR             : REAL := 15.0;
    rPrevGap_RL             : REAL := 15.0;
    rPrevGap_RR             : REAL := 15.0;
    tChokeTimer             : TON;
    bAerodynamicChoke       : BOOL := FALSE;
END_VAR

(* === MAIN SAFETY INTERLOCKS === *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bPropulsionActive := FALSE;
    rRequestedThrust := -100000.0; (* Maximum regenerative/eddy current braking *)
    bCriticalAlarm := TRUE;
    iAlarmCode := 100; (* E-STOP *)
    RETURN;
END_IF;

IF rTubePressure > rMaxTubePressure THEN
    bCriticalAlarm := TRUE;
    iAlarmCode := 101; (* Loss of vacuum *)
    rRequestedThrust := -80000.0;
    RETURN;
END_IF;

IF rSuperconductorTemp > rMaxSuperTemp THEN
    bCriticalAlarm := TRUE;
    iAlarmCode := 102; (* Quench detected *)
    rRequestedThrust := -100000.0;
    RETURN;
END_IF;

(* === ACTIVE NULL-FLUX LEVITATION CONTROL === *)
(* PID-based regulation of active levitation coils to maintain optimal gap *)
rLevitationCurrent_FL := (rNominalGap - rLevitationGap_FL) * rKp_Gap + (rPrevGap_FL - rLevitationGap_FL) * rKd_Gap;
rLevitationCurrent_FR := (rNominalGap - rLevitationGap_FR) * rKp_Gap + (rPrevGap_FR - rLevitationGap_FR) * rKd_Gap;
rLevitationCurrent_RL := (rNominalGap - rLevitationGap_RL) * rKp_Gap + (rPrevGap_RL - rLevitationGap_RL) * rKd_Gap;
rLevitationCurrent_RR := (rNominalGap - rLevitationGap_RR) * rKp_Gap + (rPrevGap_RR - rLevitationGap_RR) * rKd_Gap;

rPrevGap_FL := rLevitationGap_FL;
rPrevGap_FR := rLevitationGap_FR;
rPrevGap_RL := rLevitationGap_RL;
rPrevGap_RR := rLevitationGap_RR;

(* === AERODYNAMIC CHOKE POINT MITIGATION === *)
(* Kantrowitz limit avoidance near 1200km/h depending on tube geometry and local pressure *)
IF (rPodVelocity > 300.0) AND (rTubePressure > 50.0) THEN
    tChokeTimer(IN := TRUE, PT := T#50MS);
    IF tChokeTimer.Q THEN
        bAerodynamicChoke := TRUE;
    END_IF;
ELSE
    tChokeTimer(IN := FALSE);
    bAerodynamicChoke := FALSE;
END_IF;

(* === LINEAR SYNCHRONOUS MOTOR (LSM) STATE MACHINE === *)
CASE iStateMachine OF
    0: (* IDLE & SYSTEM CHECKS *)
        bSystemReady := TRUE;
        bPropulsionActive := FALSE;
        rRequestedThrust := 0.0;
        IF bSystemEnable THEN
            iStateMachine := 10;
        END_IF;
        
    10: (* ACCELERATION *)
        bPropulsionActive := TRUE;
        IF rPodVelocity < rTargetVelocity THEN
            rRequestedThrust := 50000.0; (* 50kN nominal thrust *)
        ELSE
            iStateMachine := 20;
        END_IF;
        
        IF bAerodynamicChoke THEN
            rRequestedThrust := 10000.0; (* Reduce thrust to pass Kantrowitz limit gently *)
        END_IF;
        
    20: (* CRUISE *)
        bPropulsionActive := TRUE;
        (* Simple P-controller for cruise speed *)
        rRequestedThrust := (rTargetVelocity - rPodVelocity) * 200.0;
        
        (* If we need to decelerate based on absolute position (e.g. approaching station) *)
        IF rPodPosition > 800000.0 THEN (* 800 km mark *)
            iStateMachine := 30;
        END_IF;
        
    30: (* DECELERATION *)
        bPropulsionActive := TRUE;
        rRequestedThrust := -40000.0;
        IF rPodVelocity < 10.0 THEN
            iStateMachine := 0;
            bSystemEnable := FALSE;
        END_IF;
        
    ELSE
        iStateMachine := 0;
END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
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
