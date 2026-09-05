import json, uuid
import os

os.makedirs("data/swarm_raw", exist_ok=True)
prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Pharmaceutical Aseptic Blow-Fill-Seal (BFS) Extruder**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., sterile parison extrusion thickness optical mapping, active mold vacuum cooling cascade, and CIP/SIP (Clean/Sterilize In Place) superheated steam lock logic). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Aseptic_BFS_Extruder\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Pharmaceutical Aseptic Blow-Fill-Seal (BFS) Extruder

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_Aseptic_BFS_Extruder_Control
VAR_INPUT
    bSystemEnable       : BOOL;     (* Master sequence enable from supervisory control *)
    bSafetyOK           : BOOL;     (* Hardwired safety relays, light curtains, and E-Stops OK *)
    rParisonThicknessSP : REAL;     (* Target setpoint for parison thickness profile in mm *)
    rParisonThicknessPV : REAL;     (* High-speed optical mapping feedback in mm *)
    rExtruderTempPV     : REAL;     (* Melt zone actual temperature in degrees Celsius *)
    bSIP_SteamReady     : BOOL;     (* Superheated steam generator at required pressure/temp *)
    bVacuumCoolingOK    : BOOL;     (* Active mold vacuum cooling cascade circulation confirmed *)
    bMoldClosed         : BOOL;     (* Position sensor feedback indicating molds are securely locked *)
END_VAR

VAR_OUTPUT
    bExtruderRun        : BOOL;     (* Command to engage the main extruder servo drive *)
    rExtruderSpeedCmd   : REAL;     (* Analog speed command (0.0 to 100.0%) to servo drive *)
    iCurrentState       : INT;      (* Current active step of the BFS master state machine *)
    bSIP_Active         : BOOL;     (* Sterilization-in-place mode active indicator for HMI *)
    bCriticalAlarm      : BOOL;     (* Critical fault requiring operator intervention *)
    bSystemReady        : BOOL;     (* System is fully sterilized and ready for production *)
END_VAR

VAR
    iState              : INT := 0; (* Internal state tracking variable *)
    tSIP_Timer          : TON;      (* Timer for sterilization hold phase *)
    tPID_Sample         : TON;      (* Sample time for parison thickness control *)
    rThicknessError     : REAL;     (* Instantaneous parison thickness deviation *)
    rIntegralAccum      : REAL := 0.0; (* Integral accumulator for PI control *)
    rProportionalTerm   : REAL;     (* P-term for thickness control *)
    rKp                 : REAL := 12.5; (* Tuning: Proportional Gain *)
    rKi                 : REAL := 1.1;  (* Tuning: Integral Gain *)
    rPID_MaxLimit       : REAL := 100.0;(* Extruder speed upper limit *)
    rPID_MinLimit       : REAL := 10.0; (* Extruder speed lower limit (prevent melt stagnation) *)
    rTargetTemp         : REAL := 175.5;(* Target extrusion temperature for pharmaceutical grade polymer *)
END_VAR

(* === MASTER SAFETY AND INTERLOCK LOGIC === *)
IF NOT bSafetyOK THEN
    bExtruderRun := FALSE;
    rExtruderSpeedCmd := 0.0;
    bSIP_Active := FALSE;
    bSystemReady := FALSE;
    bCriticalAlarm := TRUE;
    iState := 99; (* Transition to Hard Fault State *)
    iCurrentState := iState;
    RETURN;
END_IF;

(* Clear alarms if system is safe but un-enabled *)
IF NOT bSystemEnable AND iState <> 99 THEN
    bExtruderRun := FALSE;
    rExtruderSpeedCmd := 0.0;
    iState := 0;
END_IF;

(* === MAIN BFS STATE MACHINE === *)
CASE iState OF
    0: (* IDLE STATE: Waiting for enable and initial heat *)
        bSystemReady := FALSE;
        bSIP_Active := FALSE;
        IF bSystemEnable THEN
            iState := 10;
        END_IF;

    10: (* MELT PREPARATION: Wait for polymer melt temperature *)
        IF rExtruderTempPV >= rTargetTemp THEN
            (* Only proceed to Sterilization if steam is available *)
            IF bSIP_SteamReady THEN
                iState := 20;
            END_IF;
        END_IF;

    20: (* SIP PHASE: Superheated steam lock logic *)
        bSIP_Active := TRUE;
        (* Hold 121 degrees C steam for equivalent F0 time (simulated 30 minutes) *)
        tSIP_Timer(IN := TRUE, PT := T#30M);
        IF tSIP_Timer.Q THEN
            tSIP_Timer(IN := FALSE);
            bSIP_Active := FALSE;
            iState := 30;
        END_IF;

    30: (* PRODUCTION READY: Aseptic condition achieved *)
        bSystemReady := TRUE;
        IF bVacuumCoolingOK AND bMoldClosed THEN
            iState := 40;
        END_IF;

    40: (* ACTIVE EXTRUSION: Parison thickness optical mapping and PI control *)
        bExtruderRun := TRUE;
        tPID_Sample(IN := TRUE, PT := T#10MS);
        
        IF tPID_Sample.Q THEN
            tPID_Sample(IN := FALSE);
            
            (* Calculate error: SP - PV *)
            rThicknessError := rParisonThicknessSP - rParisonThicknessPV;
            
            (* Proportional term *)
            rProportionalTerm := rKp * rThicknessError;
            
            (* Integral accumulation with basic anti-windup *)
            rIntegralAccum := rIntegralAccum + (rKi * rThicknessError * 0.01);
            IF rIntegralAccum > rPID_MaxLimit THEN
                rIntegralAccum := rPID_MaxLimit;
            ELSIF rIntegralAccum < rPID_MinLimit THEN
                rIntegralAccum := rPID_MinLimit;
            END_IF;
            
            (* Calculate total control output *)
            rExtruderSpeedCmd := rProportionalTerm + rIntegralAccum;
            
            (* Clamp final output to drive limits *)
            IF rExtruderSpeedCmd > rPID_MaxLimit THEN
                rExtruderSpeedCmd := rPID_MaxLimit;
            ELSIF rExtruderSpeedCmd < rPID_MinLimit THEN
                rExtruderSpeedCmd := rPID_MinLimit;
            END_IF;
        END_IF;
        
        (* Monitor for loss of cooling or mold un-clamping during extrusion *)
        IF NOT bVacuumCoolingOK OR NOT bMoldClosed THEN
            bExtruderRun := FALSE;
            rExtruderSpeedCmd := 0.0;
            iState := 30; (* Revert to Ready state *)
        END_IF;

    99: (* FAULT STATE: Requires operator reset sequence *)
        bCriticalAlarm := TRUE;
        bExtruderRun := FALSE;
        rExtruderSpeedCmd := 0.0;
        (* Fault reset requires disabling and toggling safety *)
        IF NOT bSystemEnable THEN
            bCriticalAlarm := FALSE;
            iState := 0;
        END_IF;
        
END_CASE;

(* Output mapping *)
iCurrentState := iState;

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
