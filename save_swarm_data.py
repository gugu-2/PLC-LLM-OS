import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: High-Speed Glass Container IS (Individual Section) Machine**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., millisecond precision gob delivery tracking, parison blank mold inversion timing, blow-and-blow cycle synchronization, and infrared glass cooling rate feedback). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_IS_GlassMachine\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: High-Speed Glass Container IS (Individual Section) Machine

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_HighSpeedGlassISMachine_Control
(*
  =============================================================================
  High-Speed Glass Container IS (Individual Section) Machine Controller
  =============================================================================
  Description:
    Advanced deterministic tracking and synchronization for single-section
    blow-and-blow/press-and-blow glass forming. Handles millisecond-precision 
    gob delivery tracking, parison inversion timing, blow cycle synchronization,
    and infrared thermal feedback for closed-loop mold cooling.
  =============================================================================
*)
VAR_INPUT
    bEnable             : BOOL;     (* System master enable signal *)
    bEmergencyStop      : BOOL;     (* Safety relay OK signal (Active HIGH) *)
    rGobWeightActual    : REAL;     (* Measured gob weight in grams *)
    tGobArrivalOffset   : TIME;     (* Sync offset from shear cut to gob arrival *)
    rBlankMoldTemp      : REAL;     (* Blank mold temperature feedback (deg C) *)
    rBlowMoldTemp       : REAL;     (* Blow mold temperature feedback (deg C) *)
    rInfraredCoolRate   : REAL;     (* Post-blow infrared cooling rate (deg C/sec) *)
    bGobDetectedOptical : BOOL;     (* High-speed optical sensor for gob entry *)
END_VAR

VAR_OUTPUT
    bSystemReady        : BOOL;     (* Section ready for next shear cycle *)
    rCoolingValvePos    : REAL;     (* Proportional cooling air valve 0.0 - 100.0% *)
    bBaffleDownCmd      : BOOL;     (* Baffle mechanism lower command *)
    bInvertParisonCmd   : BOOL;     (* Neck ring invert 180-deg command *)
    bFinalBlowCmd       : BOOL;     (* Final blow high-pressure air command *)
    bTakeOutJawCmd      : BOOL;     (* Take-out mechanism grab command *)
    bRejectGob          : BOOL;     (* Defective gob/container reject chute command *)
    iSectionFaultCode   : INT;      (* 0=OK, >0=Fault Code *)
END_VAR

VAR
    iCycleState         : INT := 0; (* 0=IDLE, 10=DELIVERY, 20=BLANK, 30=INVERT, 40=BLOW, 50=TAKEOUT *)
    tCycleTimer         : TON;
    tInvertDelay        : TON;
    tCoolingTimer       : TON;
    rTempError          : REAL;
    rPID_Kp             : REAL := 2.5;
    rPID_Ki             : REAL := 0.1;
    rIntegralAccum      : REAL := 0.0;
    bCycleActive        : BOOL := FALSE;
END_VAR

(* === SAFETY & INTERLOCKS === *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bBaffleDownCmd := FALSE;
    bInvertParisonCmd := FALSE;
    bFinalBlowCmd := FALSE;
    bTakeOutJawCmd := FALSE;
    rCoolingValvePos := 100.0; (* Failsafe: max cooling on E-Stop *)
    iSectionFaultCode := 999; (* Critical E-Stop Fault *)
    iCycleState := 0;
    RETURN;
END_IF;

(* === MOLD COOLING PID CONTROL (Background Task) === *)
(* Maintain blow mold temperature at optimal 450 deg C via proportional air valve *)
rTempError := rBlowMoldTemp - 450.0;
IF rTempError > 0.0 THEN
    rIntegralAccum := rIntegralAccum + (rTempError * 0.01);
    rCoolingValvePos := (rPID_Kp * rTempError) + (rPID_Ki * rIntegralAccum);
    IF rCoolingValvePos > 100.0 THEN rCoolingValvePos := 100.0; END_IF;
    IF rCoolingValvePos < 0.0 THEN rCoolingValvePos := 0.0; END_IF;
ELSE
    rCoolingValvePos := 10.0; (* Minimum idle cooling flow *)
    rIntegralAccum := 0.0;
END_IF;

(* === MAIN IS MACHINE CYCLE STATE MACHINE === *)
CASE iCycleState OF
    0: (* IDLE - Awaiting Gob *)
        bSystemReady := TRUE;
        bBaffleDownCmd := FALSE;
        bInvertParisonCmd := FALSE;
        bFinalBlowCmd := FALSE;
        bTakeOutJawCmd := FALSE;
        bRejectGob := FALSE;
        iSectionFaultCode := 0;
        
        IF bEnable AND bGobDetectedOptical THEN
            bSystemReady := FALSE;
            bCycleActive := TRUE;
            iCycleState := 10;
        END_IF;

    10: (* GOB DELIVERY & BLANK MOLD COMPRESSION *)
        (* Gob loaded, baffle comes down to form the parison *)
        bBaffleDownCmd := TRUE;
        tCycleTimer(IN := TRUE, PT := T#250MS);
        IF tCycleTimer.Q THEN
            tCycleTimer(IN := FALSE);
            iCycleState := 20;
        END_IF;

    20: (* PARISON INVERT & TRANSFER *)
        (* Baffle up, neck ring inverts the parison to the blow mold side *)
        bBaffleDownCmd := FALSE;
        bInvertParisonCmd := TRUE;
        tInvertDelay(IN := TRUE, PT := T#650MS);
        IF tInvertDelay.Q THEN
            tInvertDelay(IN := FALSE);
            iCycleState := 30;
        END_IF;

    30: (* FINAL BLOW & THERMAL CONDITIONING *)
        (* High pressure air expands the parison, infrared scans cooling rate *)
        bFinalBlowCmd := TRUE;
        IF rInfraredCoolRate > 15.0 THEN
            (* Glass cooling too fast, thermal shock risk *)
            bRejectGob := TRUE;
            iSectionFaultCode := 401;
        END_IF;
        
        tCoolingTimer(IN := TRUE, PT := T#800MS);
        IF tCoolingTimer.Q THEN
            tCoolingTimer(IN := FALSE);
            bFinalBlowCmd := FALSE;
            iCycleState := 40;
        END_IF;

    40: (* TAKE-OUT & SWEEP *)
        (* Jaws grab the finished container and place on deadplate *)
        bInvertParisonCmd := FALSE; (* Return neck ring *)
        bTakeOutJawCmd := TRUE;
        tCycleTimer(IN := TRUE, PT := T#300MS);
        IF tCycleTimer.Q THEN
            tCycleTimer(IN := FALSE);
            bTakeOutJawCmd := FALSE;
            bCycleActive := FALSE;
            iCycleState := 0; (* Cycle Complete *)
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

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
