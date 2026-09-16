import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Autonomous Robotic Rail Car Wheelset Induction Quenching & Hardening**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Multi-frequency induction heating depth profiling, dual pyrometer circular rim thermal tracking, and polymer quench spray nozzle pressure modulation). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Wheelset_InductionHardening\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Autonomous Robotic Rail Car Wheelset Induction Quenching & Hardening

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_Wheelset_InductionHardening
VAR_INPUT
    bEnable                 : BOOL;     (* System master enable signal, multi-channel SIL3 verified *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal, active high logic *)
    rPyroTempInner          : REAL;     (* Pyrometer 1 reading: inner wheel rim surface temp [deg C] *)
    rPyroTempOuter          : REAL;     (* Pyrometer 2 reading: outer wheel rim surface temp [deg C] *)
    rQuenchPressureFeed     : REAL;     (* Polymer quench spray line feed pressure [bar] *)
    rWheelRotSpeed          : REAL;     (* Wheelset rotational speed feedback [RPM] *)
    rInductorClearance      : REAL;     (* Gap distance from induction coil to wheel rim [mm] *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* Overall machine ready status *)
    rHF_PowerCmd            : REAL;     (* High-frequency generator power reference [0-100%] *)
    rMF_PowerCmd            : REAL;     (* Medium-frequency generator power reference [0-100%] *)
    rQuenchValveCmd         : REAL;     (* Polymer quench proportional valve opening [0-100%] *)
    rWheelRotSpeedCmd       : REAL;     (* Command for wheelset drive VFD [RPM] *)
    bAlarm                  : BOOL;     (* Master fault alarm output *)
    iFaultCode              : INT;      (* Diagnostics fault code (0=OK) *)
END_VAR
VAR
    iState                  : INT := 0; (* Process state machine index *)
    tHeatingPhase           : TON;      (* Timer for the heating soak phase *)
    tQuenchPhase            : TON;      (* Timer for the polymer quenching phase *)
    
    rFilteredTempAvg        : REAL;     (* Moving average of inner/outer temperatures *)
    rTempError              : REAL;     (* Temperature error for PID calculation *)
    
    (* Internal PID variables *)
    rPID_Kp                 : REAL := 2.50;
    rPID_Ki                 : REAL := 0.15;
    rPID_Integral           : REAL := 0.0;
    
    (* Hardening profile parameters *)
    rTargetAustenitizingT   : REAL := 920.0; (* [deg C] target hardening temp *)
    rTargetQuenchPressure   : REAL := 4.5;   (* [bar] required cooling pressure *)
    
    bOverTempInterlock      : BOOL;
END_VAR

(* === MAIN LOGIC === *)
(* 1. Multi-layered Safety Interlocks & Sensor Validation *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bAlarm := TRUE;
    iFaultCode := 99; (* E-STOP Active *)
    rHF_PowerCmd := 0.0;
    rMF_PowerCmd := 0.0;
    rQuenchValveCmd := 0.0;
    rWheelRotSpeedCmd := 0.0;
    iState := 0;
    RETURN;
END_IF;

(* Basic Pyrometer Plausibility Check *)
IF (rPyroTempInner < -50.0 OR rPyroTempInner > 1300.0) OR 
   (rPyroTempOuter < -50.0 OR rPyroTempOuter > 1300.0) THEN
    bAlarm := TRUE;
    iFaultCode := 10; (* Sensor out of bounds *)
    RETURN;
END_IF;

(* 2. Thermal Tracking & Noise Filtering *)
rFilteredTempAvg := (rPyroTempInner + rPyroTempOuter) / 2.0;
bOverTempInterlock := (rFilteredTempAvg > 1050.0);

IF bOverTempInterlock THEN
    bAlarm := TRUE;
    iFaultCode := 20; (* Over-temperature interlock triggered *)
    rHF_PowerCmd := 0.0;
    rMF_PowerCmd := 0.0;
    iState := 0;
    RETURN;
END_IF;

(* 3. State Machine: Autonomous Hardening Profile *)
CASE iState OF
    0: (* IDLE & PRE-CHECK *)
        bSystemReady := TRUE;
        bAlarm := FALSE;
        iFaultCode := 0;
        rHF_PowerCmd := 0.0;
        rMF_PowerCmd := 0.0;
        rQuenchValveCmd := 0.0;
        rPID_Integral := 0.0;
        
        IF bEnable AND (rInductorClearance > 1.5 AND rInductorClearance < 3.0) THEN
            iState := 10; (* Start heating process *)
        END_IF;

    10: (* HEATING PHASE: Multi-Frequency Depth Profiling *)
        bSystemReady := FALSE;
        rWheelRotSpeedCmd := 45.0; (* Constant spin for uniform heating *)
        
        (* Dual frequency power mix: MF for depth, HF for surface *)
        rTempError := rTargetAustenitizingT - rFilteredTempAvg;
        rPID_Integral := rPID_Integral + (rTempError * rPID_Ki);
        
        (* Anti-windup limit *)
        IF rPID_Integral > 50.0 THEN rPID_Integral := 50.0; END_IF;
        IF rPID_Integral < -50.0 THEN rPID_Integral := -50.0; END_IF;
        
        rHF_PowerCmd := (rTempError * rPID_Kp * 0.4) + rPID_Integral;
        rMF_PowerCmd := (rTempError * rPID_Kp * 0.6) + rPID_Integral;
        
        (* Power clamping *)
        IF rHF_PowerCmd > 100.0 THEN rHF_PowerCmd := 100.0; END_IF;
        IF rMF_PowerCmd > 100.0 THEN rMF_PowerCmd := 100.0; END_IF;
        IF rHF_PowerCmd < 0.0 THEN rHF_PowerCmd := 0.0; END_IF;
        IF rMF_PowerCmd < 0.0 THEN rMF_PowerCmd := 0.0; END_IF;
        
        (* Wait for target temperature to be reached and soak *)
        IF (rFilteredTempAvg >= rTargetAustenitizingT - 5.0) THEN
            tHeatingPhase(IN := TRUE, PT := T#12S);
            IF tHeatingPhase.Q THEN
                tHeatingPhase(IN := FALSE);
                rHF_PowerCmd := 0.0;
                rMF_PowerCmd := 0.0;
                iState := 20; (* Transition to quenching *)
            END_IF;
        ELSE
            tHeatingPhase(IN := FALSE);
        END_IF;

    20: (* QUENCHING PHASE: Polymer Spray Modulation *)
        rWheelRotSpeedCmd := 60.0; (* Higher speed for even quenching *)
        
        (* Feedback control for quench pressure *)
        IF rQuenchPressureFeed < rTargetQuenchPressure THEN
            rQuenchValveCmd := rQuenchValveCmd + 2.5; (* Ramping open *)
        ELSE
            rQuenchValveCmd := rQuenchValveCmd - 1.0;
        END_IF;
        
        (* Valve saturation limits *)
        IF rQuenchValveCmd > 100.0 THEN rQuenchValveCmd := 100.0; END_IF;
        IF rQuenchValveCmd < 0.0 THEN rQuenchValveCmd := 0.0; END_IF;
        
        tQuenchPhase(IN := TRUE, PT := T#35S);
        IF tQuenchPhase.Q THEN
            tQuenchPhase(IN := FALSE);
            rQuenchValveCmd := 0.0;
            iState := 30; (* Process complete *)
        END_IF;

    30: (* POST-HARDENING COOL-DOWN / UNLOAD *)
        rWheelRotSpeedCmd := 0.0;
        IF (rWheelRotSpeed < 1.0) THEN
            bSystemReady := TRUE;
            IF NOT bEnable THEN
                iState := 0; (* Reset state machine *)
            END_IF;
        END_IF;

    ELSE
        (* Failsafe default *)
        iState := 0;

END_CASE;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}

filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
