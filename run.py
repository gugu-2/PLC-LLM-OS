import json
import uuid
import os

prompt = """<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Next-Gen Hypersonic Wind Tunnel Blowdown Facility**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Mach 10 contoured nozzle variable geometry throat actuation, high-enthalpy arc heater power stabilization, and pebble bed thermal storage mass flow modulation). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

CRITICAL RULES - READ EVERY LINE:
1. CODE FENCE: Use TRIPLE backticks + iec-st. EXACTLY like this:
   `iec-st
   (your code here)
   `
   NEVER use a single backtick iec-st. ALWAYS use triple backticks.
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
   code = \"\"\"`iec-st\\nFUNCTION_BLOCK FB_HypersonicWindTunnel\\n//...\\nEND_FUNCTION_BLOCK\\n`\"\"\"
   record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
   with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
       json.dump(record, f, ensure_ascii=False)
5. SELF-CHECK before saving - verify ALL:
   [ ] Fence is `iec-st
   [ ] First code line: FUNCTION_BLOCK FB_<name>
   [ ] Has VAR_INPUT section
   [ ] Has VAR_OUTPUT section
   [ ] Has END_IF; or END_CASE;
   [ ] Last code line: END_FUNCTION_BLOCK
   [ ] Closing fence: `
   [ ] Total chars >= 1500
6. REPLY with: EVOLUTION COMPLETE: Next-Gen Hypersonic Wind Tunnel Blowdown Facility

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.
</USER_REQUEST>"""

code = """`iec-st
FUNCTION_BLOCK FB_HypersonicWindTunnelControl
VAR_INPUT
    bEnableSys            : BOOL;   (* System Global Enable from Main SCADA *)
    bEmergencyStopOk      : BOOL;   (* Safety Circuit OK, Dual Channel monitored *)
    rArcHeaterTemp        : REAL;   (* High-enthalpy arc heater temp [K] *)
    rStagnationPressure   : REAL;   (* Stagnation chamber pressure [bar] *)
    rMassFlowRate         : REAL;   (* Pebble bed thermal storage mass flow [kg/s] *)
    bThroatLimitSwMax     : BOOL;   (* Variable geometry throat maximum limit switch *)
    bThroatLimitSwMin     : BOOL;   (* Variable geometry throat minimum limit switch *)
    rTargetMachNumber     : REAL;   (* Target Mach number for test section [Mach] *)
END_VAR
VAR_OUTPUT
    bSystemReady          : BOOL;   (* Facility ready for blowdown sequence *)
    rArcHeaterPowerCmd    : REAL;   (* Arc heater power output command [MW] *)
    rThroatActuatorCmd    : REAL;   (* Variable geometry throat hydraulic position command [%] *)
    bFlowValveOpen        : BOOL;   (* Main flow control valve pilot signal *)
    bCriticalAlarm        : BOOL;   (* Critical system fault active *)
    iSequenceStep         : INT;    (* Current control sequence step for HMI *)
END_VAR
VAR
    iState                : INT := 0; (* Internal state machine *)
    fbArcHeaterPID        : PID;      (* PID controller for arc heater power stabilization *)
    fbThroatPositionPID   : PID;      (* PID for variable geometry throat position *)
    tBlowdownTimer        : TON;      (* Blowdown phase duration timer *)
    tStartDelay           : TON;      (* Sequence initialization delay *)
    rFilteredPres         : REAL;     (* First-order low pass filtered stagnation pressure *)
    rFilteredTemp         : REAL;     (* First-order low pass filtered heater temperature *)
    alphaFilter           : REAL := 0.1; (* Filter coefficient for EMA noise reduction *)
    bBlowdownActive       : BOOL := FALSE;
    bSafetyTrip           : BOOL := FALSE;
END_VAR

(* === MAIN SAFETY INTERLOCKS AND NOISE FILTERING === *)
IF NOT bEmergencyStopOk THEN
    bSafetyTrip := TRUE;
    bSystemReady := FALSE;
    bCriticalAlarm := TRUE;
    bFlowValveOpen := FALSE;
    rArcHeaterPowerCmd := 0.0;
    rThroatActuatorCmd := 100.0; (* Fail safe: open throat completely *)
    iState := 999; (* FAULT STATE *)
    RETURN;
END_IF;

(* EMA Filter for critical process variables *)
rFilteredPres := (alphaFilter * rStagnationPressure) + ((1.0 - alphaFilter) * rFilteredPres);
rFilteredTemp := (alphaFilter * rArcHeaterTemp) + ((1.0 - alphaFilter) * rFilteredTemp);

(* PID parameters update (assuming initialized elsewhere with Kp, Ti, Td) *)
fbArcHeaterPID.SP := 4500.0; (* 4500 K setpoint for hypersonic enthalpy *)
fbArcHeaterPID.PV := rFilteredTemp;
fbArcHeaterPID.EN := bBlowdownActive;

fbThroatPositionPID.SP := rTargetMachNumber * 10.0; (* Simplified relationship for Mach -> Throat pos % *)
fbThroatPositionPID.PV := rFilteredPres; (* Using pressure feedback for throat adjustment loop *)
fbThroatPositionPID.EN := bBlowdownActive;

(* === MAIN CONTROL SEQUENCE === *)
CASE iState OF
    0: (* IDLE - WAIT FOR ENABLE *)
        bSystemReady := FALSE;
        bFlowValveOpen := FALSE;
        bCriticalAlarm := FALSE;
        rArcHeaterPowerCmd := 0.0;
        IF bEnableSys AND bEmergencyStopOk AND NOT bSafetyTrip THEN
            iSequenceStep := 10;
            iState := 10;
        END_IF;

    10: (* SYSTEM INITIALIZATION & SELF-TEST *)
        tStartDelay(IN := TRUE, PT := T#3S);
        IF tStartDelay.Q THEN
            tStartDelay(IN := FALSE);
            bSystemReady := TRUE;
            iSequenceStep := 20;
            IF rMassFlowRate > 0.5 THEN (* Confirm pre-flow via pebble bed *)
                iState := 20;
            END_IF;
        END_IF;

    20: (* PRE-BLOWDOWN ARC HEATER RAMP-UP *)
        fbArcHeaterPID();
        rArcHeaterPowerCmd := fbArcHeaterPID.OUT;
        
        IF rFilteredTemp > 4000.0 AND rFilteredPres > 50.0 THEN
            iSequenceStep := 30;
            iState := 30;
        END_IF;

    30: (* BLOWDOWN ACTIVE - MACH 10 NOZZLE CONTROL *)
        bBlowdownActive := TRUE;
        bFlowValveOpen := TRUE;
        
        fbArcHeaterPID();
        rArcHeaterPowerCmd := fbArcHeaterPID.OUT;
        
        fbThroatPositionPID();
        
        (* Actuator limits checking *)
        IF bThroatLimitSwMax THEN
            rThroatActuatorCmd := 100.0;
        ELSIF bThroatLimitSwMin THEN
            rThroatActuatorCmd := 0.0;
        ELSE
            rThroatActuatorCmd := fbThroatPositionPID.OUT;
        END_IF;
        
        tBlowdownTimer(IN := TRUE, PT := T#15S); (* Typical hypersonic facility run time limits *)
        
        IF tBlowdownTimer.Q OR NOT bEnableSys THEN
            bBlowdownActive := FALSE;
            bFlowValveOpen := FALSE;
            tBlowdownTimer(IN := FALSE);
            iSequenceStep := 40;
            iState := 40;
        END_IF;

    40: (* SHUTDOWN & PURGE *)
        rArcHeaterPowerCmd := 0.0;
        rThroatActuatorCmd := 100.0; (* Safe vent position *)
        
        IF rFilteredPres < 2.0 THEN
            iSequenceStep := 0;
            bSystemReady := FALSE;
            iState := 0;
        END_IF;

    999: (* FAULT HANDLING *)
        bBlowdownActive := FALSE;
        bFlowValveOpen := FALSE;
        rArcHeaterPowerCmd := 0.0;
        rThroatActuatorCmd := 100.0;
        IF bEmergencyStopOk AND bEnableSys = FALSE THEN
            bSafetyTrip := FALSE;
            bCriticalAlarm := FALSE;
            iState := 0;
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
`"""

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
