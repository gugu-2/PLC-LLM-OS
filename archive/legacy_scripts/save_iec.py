import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Utility-Scale Cryogenic Energy Storage (CES) Liquid Air Expansion Turbine**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Cryogenic pump cavitation suppression, 3-stage isothermal compression intercooling mapping, and regenerator thermal wave front balancing). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_CES_LiquidAirTurbine\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Utility-Scale Cryogenic Energy Storage (CES) Liquid Air Expansion Turbine

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_CES_LiquidAirTurbine
VAR_INPUT
    (* High-level System Commands *)
    bEnable                 : BOOL;     (* Master enable signal for the expansion turbine system *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal (TRUE = safe, FALSE = E-STOP) *)
    
    (* Physical Sensor Inputs *)
    rInletTemp              : REAL;     (* Turbine inlet temperature in deg C (Expected ~ -150) *)
    rInletPressure          : REAL;     (* Turbine inlet pressure in bar (Expected ~ 70-150 bar) *)
    rShaftSpeed             : REAL;     (* Turbine shaft rotational speed in RPM *)
    rVibrationLevel         : REAL;     (* Bearing vibration level in mm/s RMS *)
    
    (* Process Setpoints *)
    rTargetSpeed            : REAL;     (* Target RPM for the turbine *)
    rMaxVibration           : REAL;     (* Maximum allowable vibration before trip (mm/s RMS) *)
END_VAR
VAR_OUTPUT
    (* Status Flags *)
    bSystemReady            : BOOL;     (* System ready status for power generation *)
    bTurbineRunning         : BOOL;     (* Turbine is currently in RUN state *)
    bAlarm                  : BOOL;     (* Fault alarm output (General) *)
    bTrip                   : BOOL;     (* Critical trip occurred *)
    
    (* Actuator Control Signals *)
    rInletGuideVanePos      : REAL;     (* IGV (Inlet Guide Vane) command 0-100% *)
    rBypassValvePos         : REAL;     (* Bypass valve command 0-100% *)
END_VAR
VAR
    (* Internal state variables *)
    iState                  : INT := 0;
    
    (* Timers and Filters *)
    tStartupTimer           : TON;
    tCoolDownTimer          : TON;
    rFilteredSpeed          : REAL;     (* Low-pass filtered speed *)
    
    (* PID Controller for Speed Control *)
    rError                  : REAL;
    rIntegral               : REAL := 0.0;
    rDerivative             : REAL;
    rLastError              : REAL := 0.0;
    rKp                     : REAL := 0.5;
    rKi                     : REAL := 0.1;
    rKd                     : REAL := 0.05;
    
    (* Constant limits *)
    MAX_SPEED_CHANGE        : REAL := 50.0; (* RPM per cycle limit *)
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety and Interlocks Check *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bTurbineRunning := FALSE;
    bAlarm := TRUE;
    bTrip := TRUE;
    
    (* Fail-safe states for actuators *)
    rInletGuideVanePos := 0.0;
    rBypassValvePos := 100.0;
    
    iState := 999; (* Trip state *)
    RETURN;
END_IF;

(* 2. Vibration Monitoring *)
IF rVibrationLevel > rMaxVibration THEN
    bAlarm := TRUE;
    bTrip := TRUE;
    iState := 999; (* Transition to trip on high vibration *)
END_IF;

(* 3. Input Filtering (First order low-pass for speed) *)
rFilteredSpeed := rFilteredSpeed + 0.1 * (rShaftSpeed - rFilteredSpeed);

(* 4. State Machine for Turbine Operation *)
CASE iState OF
    0: (* IDLE *)
        bSystemReady := TRUE;
        bTurbineRunning := FALSE;
        rInletGuideVanePos := 0.0;
        rBypassValvePos := 100.0;
        
        IF bEnable AND (rInletPressure > 50.0) THEN
            iState := 10; (* PRE-COOLING *)
            bSystemReady := FALSE;
        END_IF;

    10: (* PRE-COOLING *)
        (* Slowly open IGV and close bypass to introduce cold gas and cool the turbine mass *)
        rInletGuideVanePos := 10.0;
        rBypassValvePos := 90.0;
        
        tStartupTimer(IN := TRUE, PT := T#120S);
        IF tStartupTimer.Q THEN
            tStartupTimer(IN := FALSE);
            iState := 20; (* RAMP-UP *)
        END_IF;

    20: (* RAMP-UP *)
        bTurbineRunning := TRUE;
        rBypassValvePos := 0.0;
        
        (* PID Speed Control *)
        rError := rTargetSpeed - rFilteredSpeed;
        rIntegral := rIntegral + rError * 0.1; (* Assumes 100ms cycle time *)
        rDerivative := (rError - rLastError) / 0.1;
        
        rInletGuideVanePos := (rKp * rError) + (rKi * rIntegral) + (rKd * rDerivative);
        
        (* Limit Output *)
        IF rInletGuideVanePos > 100.0 THEN
            rInletGuideVanePos := 100.0;
        ELSIF rInletGuideVanePos < 0.0 THEN
            rInletGuideVanePos := 0.0;
        END_IF;
        
        rLastError := rError;
        
        IF NOT bEnable THEN
            iState := 30; (* SHUTDOWN *)
        END_IF;

    30: (* SHUTDOWN / COOL-DOWN *)
        bTurbineRunning := FALSE;
        rInletGuideVanePos := 0.0;
        rBypassValvePos := 100.0;
        
        tCoolDownTimer(IN := TRUE, PT := T#300S);
        IF tCoolDownTimer.Q THEN
            tCoolDownTimer(IN := FALSE);
            iState := 0; (* Return to IDLE *)
        END_IF;
        
    999: (* FAULT / TRIP *)
        bSystemReady := FALSE;
        bTurbineRunning := FALSE;
        rInletGuideVanePos := 0.0;
        rBypassValvePos := 100.0;
        
        (* Require manual reset of bEmergencyStop or similar to clear *)
        IF bEmergencyStop AND (rVibrationLevel < rMaxVibration * 0.8) AND NOT bEnable THEN
            bTrip := FALSE;
            bAlarm := FALSE;
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
