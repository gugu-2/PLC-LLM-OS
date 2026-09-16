import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Automated Subsea Pipeline Magnetic Flux Leakage (MFL) PIG Tracking**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Extremely low frequency (ELF) electromagnetic receiver signaling, multi-valve pigging launcher sequence, and differential pressure drive speed regulation). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Subsea_MFL_PIG\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Automated Subsea Pipeline Magnetic Flux Leakage (MFL) PIG Tracking

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_Subsea_MFL_PIG_Tracker
VAR_INPUT
    (* Multi-layered safety and enablement signals *)
    bSystemEnable       : BOOL;     (* Overall system operational enable *)
    bESDOk              : BOOL;     (* Emergency Shut Down loop healthy (TRUE=OK) *)
    bLauncherDoorClosed : BOOL;     (* Pig launcher door mechanical interlock *)
    
    (* Environmental & Sensor measurements *)
    rDrivePressureDPT   : REAL;     (* Differential pressure across launcher (Bar) *)
    rFlowRate           : REAL;     (* Primary pipeline product flow rate (m^3/hr) *)
    rELFReceiverAmp     : REAL;     (* Extremely Low Frequency (ELF) antenna amplitude (mV) *)
    rELFReceiverFreq    : REAL;     (* Extremely Low Frequency (ELF) antenna frequency (Hz) *)
    rSubseaTemp         : REAL;     (* Subsea ambient temperature (Deg C) *)
    bPigPassageProxy    : BOOL;     (* Pig passage physical proxy sensor switch *)
END_VAR
VAR_OUTPUT
    (* Status and Control signals *)
    bSystemReady        : BOOL;     (* Tracking system is active and monitoring *)
    bPigLaunched        : BOOL;     (* Positive confirmation of Pig exit from launcher *)
    bPigApproaching     : BOOL;     (* ELF signal detected indicating approaching Pig *)
    rValveKickerCmd     : REAL;     (* Kicker valve analog position command 0-100% *)
    rValveMainCmd       : REAL;     (* Main pipeline valve analog position command 0-100% *)
    bCriticalAlarm      : BOOL;     (* Critical fault requiring immediate operator action *)
    iTrackingStateCode  : INT;      (* Current tracking phase state code for SCADA *)
END_VAR
VAR
    (* Internal State Machine and Timers *)
    iMainState          : INT := 0;
    iSubState           : INT := 0;
    tLaunchTimer        : TON;
    tPassageTimer       : TON;
    tELFDetectTimer     : TON;
    
    (* Filtering and Calculations *)
    rPressureFlt        : REAL := 0.0;
    rELFAmpFlt          : REAL := 0.0;
    rELFFreqFlt         : REAL := 0.0;
    rAlphaPrs           : REAL := 0.1;
    rAlphaELF           : REAL := 0.05;
    
    (* Logic flags *)
    bELFValidSignature  : BOOL;
    bDifferentialOk     : BOOL;
    bLaunchSequenceDone : BOOL;
    
    (* Limits & Constants *)
    c_rMaxLaunchPrsDPT  : REAL := 15.5;  (* Bar *)
    c_rMinLaunchPrsDPT  : REAL := 5.0;   (* Bar *)
    c_rELFNominalFreq   : REAL := 22.0;  (* Hz *)
    c_rELFFreqTol       : REAL := 2.5;   (* Hz *)
    c_rELFThresholdAmp  : REAL := 15.0;  (* mV *)
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety Interlocks & System Reset *)
IF NOT bSystemEnable OR NOT bESDOk THEN
    bSystemReady := FALSE;
    bPigLaunched := FALSE;
    bPigApproaching := FALSE;
    rValveKickerCmd := 0.0; (* Failsafe closed *)
    rValveMainCmd := 100.0; (* Failsafe open for product flow *)
    bCriticalAlarm := NOT bESDOk;
    iMainState := 0;
    iTrackingStateCode := 0;
    bLaunchSequenceDone := FALSE;
    RETURN;
END_IF;

(* 2. Sensor Noise Filtering (Exponential Moving Average) *)
rPressureFlt := (rDrivePressureDPT * rAlphaPrs) + (rPressureFlt * (1.0 - rAlphaPrs));
rELFAmpFlt   := (rELFReceiverAmp * rAlphaELF) + (rELFAmpFlt * (1.0 - rAlphaELF));
rELFFreqFlt  := (rELFReceiverFreq * rAlphaELF) + (rELFFreqFlt * (1.0 - rAlphaELF));

(* 3. Feature Extraction & Validation *)
bELFValidSignature := (rELFAmpFlt > c_rELFThresholdAmp) AND 
                      (ABS(rELFFreqFlt - c_rELFNominalFreq) < c_rELFFreqTol);

bDifferentialOk := (rPressureFlt >= c_rMinLaunchPrsDPT) AND 
                   (rPressureFlt <= c_rMaxLaunchPrsDPT);

(* 4. Main State Machine for MFL PIG Tracking *)
CASE iMainState OF
    0: (* SYSTEM INITIALIZATION & IDLE *)
        bSystemReady := TRUE;
        iTrackingStateCode := 100;
        rValveKickerCmd := 0.0; 
        IF bLauncherDoorClosed AND bSystemEnable THEN
            iMainState := 10;
        END_IF;

    10: (* KICKER VALVE SEQUENCING & PRESSURIZATION *)
        iTrackingStateCode := 200;
        IF NOT bDifferentialOk THEN
            (* Modulate kicker valve based on differential pressure (P-only control approximation) *)
            rValveKickerCmd := LIMIT(0.0, rValveKickerCmd + 0.5, 100.0);
        ELSE
            (* Pressure achieved *)
            tLaunchTimer(IN := TRUE, PT := T#30S);
            IF tLaunchTimer.Q THEN
                tLaunchTimer(IN := FALSE);
                bLaunchSequenceDone := TRUE;
                iMainState := 20;
            END_IF;
        END_IF;

    20: (* LAUNCH CONFIRMATION & TRANSIT MONITORING *)
        iTrackingStateCode := 300;
        IF bPigPassageProxy THEN
            bPigLaunched := TRUE;
            rValveKickerCmd := 0.0; (* Close kicker once launched *)
            iMainState := 30;
        END_IF;

    30: (* DEEP SEA TRANSIT & ELF LISTENING *)
        iTrackingStateCode := 400;
        tELFDetectTimer(IN := bELFValidSignature, PT := T#5S);
        IF tELFDetectTimer.Q THEN
            bPigApproaching := TRUE;
            iMainState := 40;
        ELSE
            bPigApproaching := FALSE;
        END_IF;

    40: (* APPROACH CONFIRMED & DATA SYNC PREP *)
        iTrackingStateCode := 500;
        (* Regulate main valve to manage arrival speed if necessary based on flow *)
        IF rFlowRate > 500.0 THEN
            rValveMainCmd := 85.0; (* Throttle back slightly *)
        ELSE
            rValveMainCmd := 100.0;
        END_IF;
        
        (* Completion logic or handoff to receiver station would follow... *)
        
    ELSE
        (* FAULT RECOVERY *)
        bCriticalAlarm := TRUE;
        iMainState := 0;
END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
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
