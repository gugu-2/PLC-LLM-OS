import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Supercritical CO2 Power Generation Turbine**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., extremely tight tolerance temperature/pressure cascading control at 300 bar / 700°C, extreme overspeed protection, dry gas seal regulation, and start-up sequencing). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_sCO2Turbine\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Supercritical CO2 Power Generation Turbine

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.
</USER_REQUEST>"""

code = """```iec-st
FUNCTION_BLOCK FB_sCO2TurbineMasterControl
(* 
   Supercritical CO2 Power Generation Turbine Control 
   Complex cascading control, startup sequencing, and extreme protection.
   Operating conditions: 300 bar, 700 Deg C.
*)
VAR_INPUT
    bEnableMaster       : BOOL;     (* Main operator enable signal for sCO2 turbine *)
    bEmergencyTrip      : BOOL;     (* SIL-3 certified trip circuit input (0 = TRIP) *)
    rInletTemp          : REAL;     (* Turbine inlet temperature in Deg C *)
    rInletPress         : REAL;     (* Turbine inlet pressure in Bar *)
    rRotorSpeed         : REAL;     (* Turbine rotor speed in RPM (Voting 2oo3) *)
    rSealGasPress       : REAL;     (* Dry gas seal differential pressure in Bar *)
    rBearingVibration   : REAL;     (* Primary radial bearing vibration in mm/s *)
    rExhaustTemp        : REAL;     (* Exhaust temperature in Deg C *)
END_VAR

VAR_OUTPUT
    bSystemReady        : BOOL;     (* Overall system ready for loading *)
    bStartSequenceOK    : BOOL;     (* Startup sequence complete *)
    rThrottleValveCmd   : REAL;     (* Main throttle valve position 0-100% *)
    rBypassValveCmd     : REAL;     (* Hot gas bypass valve position 0-100% *)
    bTripCommand        : BOOL;     (* Output to trip solenoid (1 = TRIP) *)
    bAlarm              : BOOL;     (* General alarm flag *)
    rActivePowerSetp    : REAL;     (* Cascaded setpoint to generator excitation *)
END_VAR

VAR
    iOpState            : INT := 0; (* Internal state machine step *)
    tSequenceTimer      : TON;      (* General sequence timer *)
    tTripTimer          : TON;      (* Trip delay timer *)
    rPidError           : REAL;     (* Speed/Pressure PID error *)
    rIntegralTerm       : REAL := 0.0;
    rDerivativeTerm     : REAL := 0.0;
    rPrevError          : REAL := 0.0;
    
    (* Constants and Limits *)
    MAX_SPEED           : REAL := 3600.0; (* Base speed RPM *)
    OVERSPEED_TRIP      : REAL := 3960.0; (* 110% overspeed *)
    MAX_INLET_TEMP      : REAL := 720.0;  (* Deg C absolute max *)
    MAX_INLET_PRESS     : REAL := 320.0;  (* Bar absolute max *)
    MIN_SEAL_PRESS      : REAL := 15.0;   (* Minimum delta pressure for seals *)
    MAX_VIBRATION       : REAL := 7.5;    (* mm/s vibration trip *)
    
    (* PID Constants *)
    KP : REAL := 0.45;
    KI : REAL := 0.12;
    KD : REAL := 0.05;
    DT : REAL := 0.01; (* 10ms execution cycle *)
END_VAR

(* === SAFETY & PROTECTION LOGIC (HIGHEST PRIORITY) === *)
IF NOT bEmergencyTrip OR 
   (rRotorSpeed > OVERSPEED_TRIP) OR 
   (rInletTemp > MAX_INLET_TEMP) OR 
   (rInletPress > MAX_INLET_PRESS) OR 
   (rSealGasPress < MIN_SEAL_PRESS) OR 
   (rBearingVibration > MAX_VIBRATION) THEN
    
    bTripCommand      := TRUE;
    bAlarm            := TRUE;
    rThrottleValveCmd := 0.0;
    rBypassValveCmd   := 100.0; (* Full bypass on trip *)
    bSystemReady      := FALSE;
    bStartSequenceOK  := FALSE;
    iOpState          := 999; (* TRIPPED STATE *)
    RETURN;
END_IF;

bTripCommand := FALSE;

(* === MAIN STATE MACHINE === *)
CASE iOpState OF
    0: (* OFF / RESET *)
        rThrottleValveCmd := 0.0;
        rBypassValveCmd := 100.0;
        bSystemReady := TRUE;
        
        IF bEnableMaster THEN
            iOpState := 10; (* Transition to Pre-Check *)
            bSystemReady := FALSE;
        END_IF;

    10: (* PRE-STARTUP CHECKS *)
        (* Verify conditions are optimal for roll-off *)
        IF (rInletPress > 150.0) AND (rInletTemp > 400.0) AND (rSealGasPress > 20.0) THEN
            iOpState := 20;
        ELSE
            bAlarm := TRUE;
        END_IF;

    20: (* WARM-UP & ROLL-OFF *)
        (* Slowly open throttle valve, modulate bypass *)
        rBypassValveCmd := rBypassValveCmd - (DT * 2.0); (* Close bypass slowly *)
        rThrottleValveCmd := rThrottleValveCmd + (DT * 1.5);
        
        IF rBypassValveCmd < 0.0 THEN rBypassValveCmd := 0.0; END_IF;
        
        IF (rRotorSpeed > 1000.0) THEN
            iOpState := 30; (* Accelerate to synchronous speed *)
        END_IF;

    30: (* ACCELERATE TO SYNCHRONOUS SPEED *)
        (* Implement PID speed control cascade to valve position *)
        rPidError := MAX_SPEED - rRotorSpeed;
        rIntegralTerm := rIntegralTerm + (rPidError * DT);
        rDerivativeTerm := (rPidError - rPrevError) / DT;
        rPrevError := rPidError;
        
        rThrottleValveCmd := (KP * rPidError) + (KI * rIntegralTerm) + (KD * rDerivativeTerm);
        
        (* Saturation checks *)
        IF rThrottleValveCmd > 100.0 THEN rThrottleValveCmd := 100.0; END_IF;
        IF rThrottleValveCmd < 5.0 THEN rThrottleValveCmd := 5.0; END_IF;
        
        IF (rRotorSpeed >= 3595.0) AND (rRotorSpeed <= 3605.0) THEN
            tSequenceTimer(IN := TRUE, PT := T#10S);
            IF tSequenceTimer.Q THEN
                tSequenceTimer(IN := FALSE);
                iOpState := 40;
            END_IF;
        ELSE
            tSequenceTimer(IN := FALSE);
        END_IF;

    40: (* LOAD GENERATION (SYNCHRONIZED) *)
        bStartSequenceOK := TRUE;
        (* In this state, we maintain speed and modulate active power setpoint *)
        rActivePowerSetp := rInletPress * 2.5; (* Simulated load calculation *)
        
        IF NOT bEnableMaster THEN
            iOpState := 50; (* Normal Shutdown *)
        END_IF;
        
    50: (* NORMAL SHUTDOWN *)
        bStartSequenceOK := FALSE;
        rThrottleValveCmd := rThrottleValveCmd - (DT * 5.0);
        rBypassValveCmd := rBypassValveCmd + (DT * 5.0);
        
        IF (rThrottleValveCmd <= 0.0) THEN
            rThrottleValveCmd := 0.0;
            IF (rRotorSpeed < 10.0) THEN
                iOpState := 0;
            END_IF;
        END_IF;
        
    999: (* TRIPPED *)
        IF NOT bEnableMaster THEN
            iOpState := 0; (* Operator must clear enable to reset *)
            bAlarm := FALSE;
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
