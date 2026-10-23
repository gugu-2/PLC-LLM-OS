import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Advanced Spacecraft Variable Specific Impulse Magnetoplasma Rocket (VASIMR)**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., ICRH (Ion Cyclotron Resonance Heating) RF power tuning, superconducting magnet cryogenic flow balancing, and plasma density variable exhaust choking). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_VASIMR_Control\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Advanced Spacecraft Variable Specific Impulse Magnetoplasma Rocket (VASIMR)

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_VASIMR_Core_Controller
VAR_INPUT
    (* Required inputs for complex control *)
    bSystemEnable       : BOOL;     (* Main propulsion system enable command *)
    bEmergencyScram     : BOOL;     (* Immediate shutdown interlock signal *)
    rPlasmaDensityIn    : REAL;     (* Measured neutral gas plasma density [kg/m^3] *)
    rRfPowerCommand     : REAL;     (* Desired RF heating power [kW] for ICRH *)
    rMagneticFieldStr   : REAL;     (* Superconducting magnetic field strength [T] *)
    rCryoCoolantFlow    : REAL;     (* Cryogenic mass flow rate [kg/s] *)
    rExhaustTemp        : REAL;     (* Plasma exhaust temp [K] *)
    bAutoTuneEnable     : BOOL;     (* Enable automatic RF impedance matching *)
END_VAR
VAR_OUTPUT
    (* Required outputs *)
    bSystemReady        : BOOL;     (* Thruster armed and ready for ignition *)
    rHeliconPowerOut    : REAL;     (* Helicon coupler RF power output setpoint [kW] *)
    rIcrhPowerOut       : REAL;     (* Ion Cyclotron Resonance Heating power [kW] *)
    rMagneticChokeOut   : REAL;     (* Variable magnetic nozzle choke field [T] *)
    bCryoFaultAlarm     : BOOL;     (* Cryogenic cooling system fault detected *)
    bPlasmaInstability  : BOOL;     (* Plasma instability warning *)
    iOperatingState     : INT;      (* Current operating state machine step *)
END_VAR
VAR
    (* Internal state variables *)
    tStartupTimer       : TON;
    tFaultTimer         : TON;
    rIntegralError      : REAL := 0.0;
    rDerivativeError    : REAL := 0.0;
    rLastError          : REAL := 0.0;
    rGainProportional   : REAL := 2.5;
    rGainIntegral       : REAL := 0.15;
    rGainDerivative     : REAL := 0.05;
    rPidOutput          : REAL := 0.0;
    rTargetDensity      : REAL := 1.2E-5;
    rDensityError       : REAL;
    iState              : INT := 0;
END_VAR

(* === MAIN LOGIC === *)
(* Emergency SCRAM overriding all other states *)
IF bEmergencyScram THEN
    bSystemReady        := FALSE;
    rHeliconPowerOut    := 0.0;
    rIcrhPowerOut       := 0.0;
    rMagneticChokeOut   := 0.0;
    bCryoFaultAlarm     := FALSE;
    bPlasmaInstability  := FALSE;
    iOperatingState     := 999; (* Fault state *)
    iState              := 0;
    rIntegralError      := 0.0;
    RETURN;
END_IF;

(* Monitor cryogenic system health *)
IF (rCryoCoolantFlow < 0.05) AND (rMagneticFieldStr > 1.0) THEN
    tFaultTimer(IN := TRUE, PT := T#2S);
    IF tFaultTimer.Q THEN
        bCryoFaultAlarm := TRUE;
        bSystemReady := FALSE;
        rIcrhPowerOut := 0.0;
        iState := 999; (* Drop to fault *)
    END_IF;
ELSE
    tFaultTimer(IN := FALSE);
    bCryoFaultAlarm := FALSE;
END_IF;

(* VASIMR State Machine Control *)
CASE iState OF
    0: (* IDLE & SAFE *)
        bSystemReady := FALSE;
        rHeliconPowerOut := 0.0;
        rIcrhPowerOut := 0.0;
        rMagneticChokeOut := rMagneticFieldStr * 0.1; (* Standby choke *)
        iOperatingState := 0;
        
        IF bSystemEnable AND NOT bCryoFaultAlarm THEN
            iState := 10;
            tStartupTimer(IN := FALSE);
        END_IF;

    10: (* MAGNETIC FIELD RAMP UP *)
        iOperatingState := 10;
        rMagneticChokeOut := rMagneticFieldStr * 0.5;
        tStartupTimer(IN := TRUE, PT := T#10S);
        
        IF tStartupTimer.Q AND (rMagneticFieldStr > 1.5) THEN
            tStartupTimer(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* PLASMA GENERATION (HELICON) *)
        iOperatingState := 20;
        rHeliconPowerOut := 50.0; (* 50 kW to initialize plasma *)
        
        IF rPlasmaDensityIn > 0.8E-5 THEN
            iState := 30;
        ELSIF tStartupTimer.Q THEN
            bPlasmaInstability := TRUE;
            iState := 0;
        END_IF;

    30: (* ICRH ACCELERATION & TUNING *)
        iOperatingState := 30;
        bSystemReady := TRUE;
        
        (* PID Control for Plasma Density via RF Power *)
        rDensityError := rTargetDensity - rPlasmaDensityIn;
        rIntegralError := rIntegralError + rDensityError;
        rDerivativeError := rDensityError - rLastError;
        
        rPidOutput := (rGainProportional * rDensityError) + 
                      (rGainIntegral * rIntegralError) + 
                      (rGainDerivative * rDerivativeError);
                      
        rLastError := rDensityError;
        
        IF bAutoTuneEnable THEN
            rIcrhPowerOut := rRfPowerCommand + rPidOutput;
        ELSE
            rIcrhPowerOut := rRfPowerCommand;
        END_IF;
        
        (* Saturation limits for safety *)
        IF rIcrhPowerOut > 2000.0 THEN
            rIcrhPowerOut := 2000.0;
        ELSIF rIcrhPowerOut < 0.0 THEN
            rIcrhPowerOut := 0.0;
        END_IF;
        
        (* Variable Magnetic Nozzle Control *)
        rMagneticChokeOut := (rExhaustTemp / 50000.0) * rMagneticFieldStr;

        IF NOT bSystemEnable THEN
            iState := 40;
        END_IF;

    40: (* SHUTDOWN SEQUENCE *)
        iOperatingState := 40;
        rIcrhPowerOut := 0.0;
        rHeliconPowerOut := rHeliconPowerOut * 0.5;
        
        tStartupTimer(IN := TRUE, PT := T#5S);
        IF tStartupTimer.Q THEN
            tStartupTimer(IN := FALSE);
            iState := 0;
        END_IF;
        
    999: (* FAULT HANDLING *)
        iOperatingState := 999;
        rIcrhPowerOut := 0.0;
        rHeliconPowerOut := 0.0;
        rMagneticChokeOut := 0.0;
        bSystemReady := FALSE;
        
        IF NOT bCryoFaultAlarm AND NOT bEmergencyScram AND NOT bSystemEnable THEN
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
