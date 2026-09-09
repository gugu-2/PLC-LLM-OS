import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Advanced Spacecraft Ionospheric Plasma Electrodynamic Tether**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 10km conductive orbital tether voltage cascade, Lorentz force orbital drag/boost compensation, and micro-meteoroid severance detection). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_ElectrodynamicTether\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Advanced Spacecraft Ionospheric Plasma Electrodynamic Tether

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_ElectrodynamicTether
VAR_INPUT
    (* Physical system inputs *)
    bEnable                : BOOL;     (* Main system enable command for the tether sequence *)
    bEmergencyStop         : BOOL;     (* Hardwire safety relay OK signal; FALSE = abort all ops *)
    rTetherVoltage         : REAL;     (* Measured voltage potential across 10km tether (Volts) *)
    rPlasmaDensity         : REAL;     (* Local ionospheric plasma density (particles/cm^3) *)
    rOrbitalVelocity       : REAL;     (* Spacecraft orbital velocity vector magnitude (m/s) *)
    rLocalMagneticField    : REAL;     (* Earth magnetic field orthogonal component (Tesla) *)
    bMicrometeoroidImpact  : BOOL;     (* Acoustic/Optical impact detection flag on tether reel *)
    rTetherTension         : REAL;     (* Mechanical tension on tether deployment reel (Newtons) *)
END_VAR
VAR_OUTPUT
    (* Control system outputs *)
    bSystemReady           : BOOL;     (* Tether control system initialized and ready for boost *)
    rLorentzForceTarget    : REAL;     (* Calculated target thrust/drag force to actuators (N) *)
    rCathodeEmissionCmd    : REAL;     (* Current command for Hollow Cathode Assembly (Amperes) *)
    bTetherSeveranceAlarm  : BOOL;     (* FATAL: Tether severance detected (Sudden tension loss) *)
    bOvervoltageFault      : BOOL;     (* ERROR: Cascade voltage exceeded maximum dielectric limits *)
    iActiveState           : INT;      (* Current operational state machine step for telemetry *)
END_VAR
VAR
    (* Internal state variables and timers *)
    iState                 : INT := 0; (* Internal state machine *)
    tSafetyTimer           : TON;      (* Overvoltage integration timer to filter spikes *)
    tFaultDelay            : TON;      (* Severance confirmation timer to prevent false positives *)
    rEffectiveLength       : REAL := 10000.0; (* Fully deployed tether length in meters (10 km) *)
    rInducedVoltage        : REAL;     (* Calculated motional EMF: v x B * L *)
    rVoltageError          : REAL;     (* PID Error term for voltage matching *)
    rProportionalGain      : REAL := 0.015; (* P-gain for cathode emission control loop *)
    bFaultLatch            : BOOL := FALSE; (* Global fault latch for safe state lockout *)
END_VAR

(* === ADVANCED LORENTZ FORCE & TETHER CONTROL LOGIC === *)

(* 1. Safety Interlocks & Hard Fault Evaluation *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    rCathodeEmissionCmd := 0.0;
    rLorentzForceTarget := 0.0;
    iActiveState := 999;
    RETURN;
END_IF;

(* 2. Micrometeoroid Impact & Severance Detection *)
(* If impact is detected AND tension drops below 0.1 N, flag severance *)
IF bMicrometeoroidImpact AND (rTetherTension < 0.1) THEN
    tFaultDelay(IN := TRUE, PT := T#500MS);
    IF tFaultDelay.Q THEN
        bTetherSeveranceAlarm := TRUE;
        bFaultLatch := TRUE;
    END_IF;
ELSE
    tFaultDelay(IN := FALSE);
END_IF;

(* 3. Electrodynamic Overvoltage Monitoring *)
(* Monitor cascade overvoltage risks in dense plasma regions (> 5kV threshold) *)
IF ABS(rTetherVoltage) > 5000.0 THEN
    tSafetyTimer(IN := TRUE, PT := T#2S);
    IF tSafetyTimer.Q THEN
        bOvervoltageFault := TRUE;
        bFaultLatch := TRUE;
    END_IF;
ELSE
    tSafetyTimer(IN := FALSE);
END_IF;

(* Fail-safe shutdown on any latched fault *)
IF bFaultLatch THEN
    iState := 99;
END_IF;

(* 4. Main Electrodynamic State Machine *)
CASE iState OF
    0: (* SYSTEM IDLE / STANDBY *)
        bSystemReady := FALSE;
        rCathodeEmissionCmd := 0.0;
        rLorentzForceTarget := 0.0;
        
        IF bEnable AND NOT bFaultLatch THEN
            iState := 10;
        END_IF;

    10: (* INITIALIZATION & PLASMA DIAGNOSTICS *)
        (* Wait for minimum plasma density to establish reliable electrical connection *)
        IF rPlasmaDensity > 1000.0 THEN
            bSystemReady := TRUE;
            iState := 20;
        END_IF;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    20: (* ACTIVE LORENTZ BOOST / DRAG CONTROL *)
        (* Calculate theoretically induced Motional EMF: V = v * B * L *)
        rInducedVoltage := rOrbitalVelocity * rLocalMagneticField * rEffectiveLength;
        
        (* Calculate error between measured potential and theoretical EMF *)
        rVoltageError := rInducedVoltage - rTetherVoltage;
        
        (* Compute required electron emission current to maintain circuit (A) *)
        (* Using simple proportional control for Hollow Cathode emission *)
        rCathodeEmissionCmd := rVoltageError * rProportionalGain;
        
        (* Clamp Cathode Emission Current to safe hardware limits (0.0A - 10.0A) *)
        IF rCathodeEmissionCmd > 10.0 THEN
            rCathodeEmissionCmd := 10.0;
        ELSIF rCathodeEmissionCmd < 0.0 THEN
            rCathodeEmissionCmd := 0.0;
        END_IF;
        
        (* Calculate resulting Lorentz Force: F = I * L x B *)
        rLorentzForceTarget := rCathodeEmissionCmd * rEffectiveLength * rLocalMagneticField;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    99: (* FAULT HANDLING STATE *)
        bSystemReady := FALSE;
        rCathodeEmissionCmd := 0.0;
        rLorentzForceTarget := 0.0;
        
        (* Require system disable and fault clear before restart *)
        IF NOT bEnable AND NOT bOvervoltageFault AND NOT bTetherSeveranceAlarm THEN
            bFaultLatch := FALSE;
            iState := 0;
        END_IF;

END_CASE;

(* Update Output State Telemetry *)
iActiveState := iState;

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
