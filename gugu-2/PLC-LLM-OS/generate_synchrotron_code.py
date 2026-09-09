import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Advanced Synchrotron Light Source Undulator Insertion Device**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 10-micron permanent magnet gap servo control, bremsstrahlung radiation active shielding interlocks, and continuous top-up injection electron beam matching). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_SynchrotronUndulator\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Advanced Synchrotron Light Source Undulator Insertion Device

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_SynchrotronUndulator_Ctrl
(* 
   =============================================================================
   Block Name    : FB_SynchrotronUndulator_Ctrl
   Description   : Advanced Synchrotron Light Source Undulator Insertion Device 
                   10-micron permanent magnet gap servo control, bremsstrahlung 
                   radiation active shielding interlocks, and continuous top-up 
                   injection electron beam matching.
   Author        : 40-Year Veteran PLC Architect
   Date          : 2026-09-10
   ============================================================================= 
*)
VAR_INPUT
    bSystemEnable         : BOOL;  (* Global system enable signal for undulator control *)
    bTopUpInjectionActive : BOOL;  (* Indicates active continuous top-up injection mode *)
    rRequestedGap         : REAL;  (* Desired magnet gap in mm (precision to 0.001 mm) *)
    rActualGapPos         : REAL;  (* Actual gap position from absolute linear encoders *)
    rBeamEnergyMeV        : REAL;  (* Real-time electron beam energy in MeV *)
    rBremsstrahlungLevel  : REAL;  (* Radiation monitor level for bremsstrahlung in mSv/h *)
    bSafetyInterlockOK    : BOOL;  (* Safety chain status including hutch doors and e-stops *)
    bShieldingActive      : BOOL;  (* Status of active movable radiation shielding *)
END_VAR
VAR_OUTPUT
    bGapServoEnable       : BOOL;  (* Enable signal to gap servo drives *)
    rGapServoCmd          : REAL;  (* Position command to servo drives (mm) *)
    bBeamDumpRequest      : BOOL;  (* Critical safety request to dump the electron beam *)
    bSystemReady          : BOOL;  (* Undulator is ready for beam physics experiments *)
    iOperatingState       : INT;   (* Current state machine step *)
    bWarningAlarm         : BOOL;  (* Non-critical warning (e.g., following error) *)
END_VAR
VAR
    (* Internal State and Timers *)
    iState                : INT := 0;
    tTopUpTimer           : TON;
    tInterlockTimer       : TON;
    tMotionTimeout        : TON;
    rPositionError        : REAL;
    
    (* Constants *)
    rMAX_GAP              : REAL := 150.0; (* mm *)
    rMIN_GAP              : REAL := 4.500; (* mm *)
    rTOLERANCE            : REAL := 0.010; (* 10 microns *)
    rMAX_RADIATION        : REAL := 5.0;   (* mSv/h trip level *)
END_VAR

(* === MAIN SAFETY INTERLOCK LOGIC === *)
(* Immediate reaction to safety violations *)
IF NOT bSafetyInterlockOK OR (rBremsstrahlungLevel > rMAX_RADIATION AND NOT bShieldingActive) THEN
    bGapServoEnable := FALSE;
    bBeamDumpRequest := TRUE;
    bSystemReady := FALSE;
    iOperatingState := -1; (* FAULT STATE *)
    bWarningAlarm := TRUE;
    RETURN;
END_IF;

(* Clear Beam Dump if safety is restored *)
bBeamDumpRequest := FALSE;

(* === CONTINUOUS TOP-UP INJECTION MATCHING === *)
(* During top-up, we may need to freeze or slightly widen the gap to avoid disturbing injection *)
IF bTopUpInjectionActive THEN
    tTopUpTimer(IN := TRUE, PT := T#2S);
    IF NOT tTopUpTimer.Q THEN
        (* Freeze motion during the initial transient of injection *)
        rGapServoCmd := rActualGapPos; 
        bSystemReady := FALSE;
        bWarningAlarm := TRUE; (* Indicate top-up disturbance *)
        RETURN;
    END_IF;
ELSE
    tTopUpTimer(IN := FALSE);
END_IF;

(* === GAP CONTROL STATE MACHINE === *)
rPositionError := ABS(rRequestedGap - rActualGapPos);

CASE iState OF
    0: (* IDLE & INITIALIZATION *)
        bGapServoEnable := FALSE;
        bSystemReady := FALSE;
        bWarningAlarm := FALSE;
        IF bSystemEnable THEN
            iState := 10;
        END_IF;

    10: (* PARAMETER VALIDATION *)
        IF (rRequestedGap >= rMIN_GAP) AND (rRequestedGap <= rMAX_GAP) THEN
            iState := 20;
        ELSE
            bWarningAlarm := TRUE;
            iState := 0;
        END_IF;

    20: (* SERVO ENABLE & MOTION PROFILING *)
        bGapServoEnable := TRUE;
        rGapServoCmd := rRequestedGap;
        
        tMotionTimeout(IN := TRUE, PT := T#15S);
        
        IF rPositionError <= rTOLERANCE THEN
            tMotionTimeout(IN := FALSE);
            iState := 30;
        ELSIF tMotionTimeout.Q THEN
            (* Motion took too long - possible mechanical jam *)
            tMotionTimeout(IN := FALSE);
            bGapServoEnable := FALSE;
            bWarningAlarm := TRUE;
            iState := 0; 
        END_IF;

    30: (* IN POSITION - SYSTEM READY *)
        bSystemReady := TRUE;
        
        (* Monitor for deviations or new commands *)
        IF (rPositionError > rTOLERANCE * 2.0) OR (rRequestedGap <> rGapServoCmd) THEN
            bSystemReady := FALSE;
            iState := 10;
        END_IF;
        
        IF NOT bSystemEnable THEN
            iState := 0;
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

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
