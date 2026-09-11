import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: High-Speed Maglev Train Superconducting Electromagnetic Levitation**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Cryocooler absolute zero thermal profiling, active guideway multi-axis gap clearance (millimeters at 600km/h), and quenching fault-tolerance cascading logic). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_MaglevLevitation\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: High-Speed Maglev Train Superconducting Electromagnetic Levitation

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_MaglevSuperconductingLevitationControl
VAR_INPUT
    bSystemEnable           : BOOL;     (* Main safety enable signal for the levitation control subsystem *)
    bEmergencyStop          : BOOL;     (* Hardware E-stop circuit OK signal (active high) *)
    rGapClearanceZ          : REAL;     (* Measured vertical guideway gap in millimeters (resolution: 0.01mm) *)
    rGapClearanceY          : REAL;     (* Measured lateral guideway gap in millimeters (resolution: 0.01mm) *)
    rTrainVelocity          : REAL;     (* Train instantaneous velocity in km/h *)
    rCryostatTemp           : REAL;     (* Absolute temperature of superconducting coil cryostat in Kelvin *)
    rLiquidHeliumLevel      : REAL;     (* Percentage of liquid helium remaining in primary cooling bath *)
    rSuperconductorCurrent  : REAL;     (* Real-time excitation current passing through SC coils in Amperes *)
END_VAR

VAR_OUTPUT
    bLevitationReady        : BOOL;     (* Indicates system is fully cooled, stable, and ready for levitation *)
    rCoilVoltageCommand     : REAL;     (* Commanded control voltage to main superconducting coil power supply *)
    bQuenchAlarm            : BOOL;     (* Critical alarm indicating incipient or active superconducting quench *)
    bCryoFault              : BOOL;     (* Alarm indicating cooling system failure or low helium levels *)
    iOperatingState         : INT;      (* Current state machine step of the levitation controller *)
    rActiveDampingY         : REAL;     (* Lateral electromagnetic damping force command in kN *)
END_VAR

VAR
    (* Internal State and Timers *)
    iState                  : INT := 0; (* 0: Power-Off/Fault, 10: Cooling, 20: Pre-Excitation, 30: Levitating, 99: Quench/Fault *)
    tCoolingTimer           : TON;
    tStabilityTimer         : TON;
    tQuenchMonitor          : TON;

    (* Constants and Limits *)
    c_rTargetGapZ           : REAL := 12.0;     (* Target vertical levitation gap (mm) *)
    c_rMaxGapDeviation      : REAL := 2.5;      (* Maximum allowable vertical deviation before fault (mm) *)
    c_rCriticalTemp         : REAL := 4.2;      (* Critical superconducting threshold temperature (K) *)
    c_rMaxTempWarning       : REAL := 4.5;      (* Temperature warning threshold indicating cooling stress (K) *)
    c_rCriticalCurrentMax   : REAL := 5000.0;   (* Maximum allowable operating current before quench risk (A) *)
    
    (* Control Variables *)
    rErrorZ                 : REAL := 0.0;
    rDerivativeZ            : REAL := 0.0;
    rIntegralZ              : REAL := 0.0;
    rPrevErrorZ             : REAL := 0.0;
    
    (* PID Gains - Gain Scheduled based on velocity *)
    rKp_Z                   : REAL := 250.0;
    rKi_Z                   : REAL := 50.0;
    rKd_Z                   : REAL := 120.0;
END_VAR

(* === MAIN SAFETY AND INTERLOCK LOGIC === *)
IF NOT bEmergencyStop THEN
    bLevitationReady := FALSE;
    bQuenchAlarm := FALSE;
    iState := 0;
    rCoilVoltageCommand := 0.0;
    rActiveDampingY := 0.0;
    RETURN;
END_IF;

(* Continuous Quench Protection Monitoring *)
IF (rCryostatTemp > c_rCriticalTemp AND rSuperconductorCurrent > 100.0) OR (rSuperconductorCurrent > c_rCriticalCurrentMax) THEN
    bQuenchAlarm := TRUE;
    iState := 99; (* Force fault state *)
END_IF;

(* Continuous Cryo Diagnostics *)
IF rLiquidHeliumLevel < 15.0 OR rCryostatTemp > c_rMaxTempWarning THEN
    bCryoFault := TRUE;
ELSE
    bCryoFault := FALSE;
END_IF;

(* === MAIN STATE MACHINE === *)
CASE iState OF
    0: (* IDLE / POWER OFF *)
        bLevitationReady := FALSE;
        rCoilVoltageCommand := 0.0;
        rActiveDampingY := 0.0;
        
        IF bSystemEnable AND NOT bQuenchAlarm AND NOT bCryoFault THEN
            iState := 10;
        END_IF;

    10: (* COOLING AND THERMAL STABILIZATION *)
        (* Wait for absolute zero profiling to ensure coil is fully superconducting *)
        tCoolingTimer(IN := (rCryostatTemp <= c_rCriticalTemp), PT := T#30S);
        
        IF tCoolingTimer.Q THEN
            tCoolingTimer(IN := FALSE);
            iState := 20;
        ELSIF NOT (rCryostatTemp <= c_rCriticalTemp) THEN
            tCoolingTimer(IN := FALSE);
        END_IF;
        
        IF NOT bSystemEnable THEN
            iState := 0;
        END_IF;

    20: (* PRE-EXCITATION / FIELD RAMP-UP *)
        (* Slowly ramp up coil current while resting on physical support guideway *)
        bLevitationReady := TRUE;
        
        IF rTrainVelocity > 1.0 THEN
            iState := 30; (* Train is beginning to move, switch to active levitation *)
        END_IF;
        
        IF NOT bSystemEnable THEN
            iState := 0;
        END_IF;

    30: (* ACTIVE LEVITATION AND GAP CLEARANCE CONTROL *)
        (* High-Speed Multi-Axis PID Control *)
        rErrorZ := c_rTargetGapZ - rGapClearanceZ;
        rDerivativeZ := rErrorZ - rPrevErrorZ;
        rIntegralZ := rIntegralZ + rErrorZ;
        
        (* Gain Scheduling: Stiffen control at higher speeds (600 km/h) *)
        IF rTrainVelocity > 300.0 THEN
            rKp_Z := 400.0;
            rKd_Z := 200.0;
        ELSE
            rKp_Z := 250.0;
            rKd_Z := 120.0;
        END_IF;

        (* Calculate commanded coil voltage (actuation) *)
        rCoilVoltageCommand := (rKp_Z * rErrorZ) + (rKi_Z * rIntegralZ) + (rKd_Z * rDerivativeZ);
        rPrevErrorZ := rErrorZ;
        
        (* Lateral Active Damping calculation (simplified proportional) *)
        rActiveDampingY := rGapClearanceY * (-150.0);
        
        (* Fault detection for mechanical gap violation *)
        IF ABS(rErrorZ) > c_rMaxGapDeviation THEN
            tStabilityTimer(IN := TRUE, PT := T#100MS);
            IF tStabilityTimer.Q THEN
                iState := 99; (* Loss of levitation stability *)
            END_IF;
        ELSE
            tStabilityTimer(IN := FALSE);
        END_IF;

    99: (* FAULT / QUENCH / SHUTDOWN *)
        (* Safe cascade shutdown of energy in the superconducting coil *)
        bLevitationReady := FALSE;
        rCoilVoltageCommand := -100.0; (* Active fast discharge *)
        rActiveDampingY := 0.0;
        
        IF rSuperconductorCurrent < 10.0 AND NOT bQuenchAlarm AND bSystemEnable THEN
            iState := 0; (* Allowed to reset if fault cleared *)
        END_IF;

END_CASE;

iOperatingState := iState;

END_FUNCTION_BLOCK
```"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}

os.makedirs("c:/Users/majip/Downloads/LLM REASEARCH/data/swarm_raw", exist_ok=True)
filename = f"c:/Users/majip/Downloads/LLM REASEARCH/data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
