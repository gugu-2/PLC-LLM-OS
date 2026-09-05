import json, uuid, os

prompt = """<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Automated Submarine Optical Fiber Cable Repeater Splicing Jointing**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Erbium-doped fiber amplifier (EDFA) core alignment optical coherence, 20-MPa hydrostatic pressure vessel sealing sequences, and extreme low-loss splice attenuation validation). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

CRITICAL RULES - READ EVERY LINE:
1. CODE FENCE: Use TRIPLE backticks + iec-st. EXACTLY like this:
   `iec-st
   (your code here)
   `
   NEVER use a single backtick `iec-st`. ALWAYS use triple backticks.
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
   code = \"\"\"`iec-st\\nFUNCTION_BLOCK FB_SubmarineRepeaterSplicing\\n//...\\nEND_FUNCTION_BLOCK\\n`\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Automated Submarine Optical Fiber Cable Repeater Splicing Jointing

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.
</USER_REQUEST>"""

code = """`iec-st
FUNCTION_BLOCK FB_SubmarineRepeaterSplicing
VAR_INPUT
    bEnable                 : BOOL;     (* System enable signal for the splicing sequence *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal; TRUE = Safe to operate *)
    rHydrostaticPressure    : REAL;     (* Current pressure inside the chamber [MPa] *)
    rCoreAlignmentTolerance : REAL;     (* Maximum allowed offset for EDFA fiber core [um] *)
    rFiberPositionX         : REAL;     (* Real-time X-axis position of fiber 1 [um] *)
    rFiberPositionY         : REAL;     (* Real-time Y-axis position of fiber 1 [um] *)
    rOpticalAttenuation     : REAL;     (* Splice loss reading from OTDR [dB] *)
    bSealIntegrityCheck     : BOOL;     (* Seal verification signal from Helium leak detector *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* System ready status; all interlocks clear *)
    rArcCurrentOutput       : REAL;     (* Regulated current output for splicing arc [mA] *)
    rArcDurationOutput      : REAL;     (* Regulated duration output for splicing arc [ms] *)
    bSpliceAccepted         : BOOL;     (* Final quality check result: TRUE if splice is within limits *)
    bChamberSealed          : BOOL;     (* TRUE when hydrostatic pressure vessel is sealed and verified *)
    bAlarm                  : BOOL;     (* Fault alarm output; TRUE indicates failure mode *)
    iErrorCode              : INT;      (* Detailed error code for diagnostics *)
END_VAR
VAR
    iState                  : INT := 0; 
    tArcTimer               : TON;
    tSealTimer              : TON;
    rCurrentAlignErrorX     : REAL;
    rCurrentAlignErrorY     : REAL;
    rTotalAlignError        : REAL;
    bArcActive              : BOOL := FALSE;
    bPreFusionComplete      : BOOL := FALSE;
END_VAR

(* === MAIN LOGIC === *)
(* Emergency stop and interlock evaluation *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bAlarm := TRUE;
    iErrorCode := 999; (* Critical Safety Interlock Tripped *)
    iState := 0;
    rArcCurrentOutput := 0.0;
    rArcDurationOutput := 0.0;
    RETURN;
END_IF;

(* Clear basic alarms if emergency stop is healthy *)
bAlarm := FALSE;
iErrorCode := 0;

CASE iState OF
    0: (* IDLE & INITIALIZATION *)
        bSystemReady := TRUE;
        bSpliceAccepted := FALSE;
        bChamberSealed := FALSE;
        bPreFusionComplete := FALSE;
        rArcCurrentOutput := 0.0;
        rArcDurationOutput := 0.0;
        
        IF bEnable THEN
            bSystemReady := FALSE;
            iState := 10;
        END_IF;

    10: (* CORE ALIGNMENT SEQUENCE *)
        (* Calculate geometric core offset using Pythagoras approximation for fast evaluation *)
        rCurrentAlignErrorX := ABS(rFiberPositionX);
        rCurrentAlignErrorY := ABS(rFiberPositionY);
        
        (* In a real mathematical context we would use SQRT, this is a simplified safety check *)
        rTotalAlignError := (rCurrentAlignErrorX * rCurrentAlignErrorX) + (rCurrentAlignErrorY * rCurrentAlignErrorY);
        
        IF rTotalAlignError <= (rCoreAlignmentTolerance * rCoreAlignmentTolerance) THEN
            iState := 20; (* Alignment within tolerance, proceed to pre-fusion *)
        ELSIF rTotalAlignError > 100.0 THEN
            bAlarm := TRUE;
            iErrorCode := 101; (* Gross alignment failure *)
            iState := 900; (* Fault state *)
        END_IF;

    20: (* PRE-FUSION ARC *)
        IF NOT bPreFusionComplete THEN
            rArcCurrentOutput := 12.5; (* Pre-fusion current [mA] *)
            rArcDurationOutput := 200.0; (* Pre-fusion duration [ms] *)
            tArcTimer(IN := TRUE, PT := T#200MS);
            
            IF tArcTimer.Q THEN
                tArcTimer(IN := FALSE);
                bPreFusionComplete := TRUE;
                rArcCurrentOutput := 0.0;
                rArcDurationOutput := 0.0;
            END_IF;
        ELSE
            iState := 30; (* Proceed to Main Fusion *)
        END_IF;

    30: (* MAIN FUSION ARC *)
        rArcCurrentOutput := 16.8; (* Main fusion current for EDFA fiber [mA] *)
        rArcDurationOutput := 2500.0; (* Main fusion duration [ms] *)
        tArcTimer(IN := TRUE, PT := T#2500MS);
        
        IF tArcTimer.Q THEN
            tArcTimer(IN := FALSE);
            rArcCurrentOutput := 0.0;
            rArcDurationOutput := 0.0;
            iState := 40;
        END_IF;

    40: (* SPLICE ATTENUATION VALIDATION *)
        (* Target splice loss is strictly < 0.02 dB for transoceanic repeaters *)
        IF rOpticalAttenuation < 0.02 THEN
            bSpliceAccepted := TRUE;
            iState := 50; (* Proceed to vessel sealing *)
        ELSE
            bSpliceAccepted := FALSE;
            bAlarm := TRUE;
            iErrorCode := 102; (* Splice loss too high *)
            iState := 900; (* Fault state *)
        END_IF;

    50: (* HYDROSTATIC VESSEL SEALING & PRESSURIZATION *)
        (* Target hydrostatic pressure for deep sea deployment is around 20 MPa *)
        IF rHydrostaticPressure >= 20.0 AND bSealIntegrityCheck THEN
            tSealTimer(IN := TRUE, PT := T#10S); (* Hold for verification *)
            IF tSealTimer.Q THEN
                tSealTimer(IN := FALSE);
                bChamberSealed := TRUE;
                iState := 60;
            END_IF;
        ELSIF rHydrostaticPressure < 20.0 THEN
            (* Waiting for pressurization system to reach target *)
            tSealTimer(IN := FALSE);
        ELSE
            bAlarm := TRUE;
            iErrorCode := 103; (* Seal integrity failure during pressure test *)
            iState := 900;
        END_IF;

    60: (* COMPLETE *)
        bSystemReady := TRUE;
        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    900: (* FAULT HANDLING *)
        rArcCurrentOutput := 0.0;
        rArcDurationOutput := 0.0;
        tArcTimer(IN := FALSE);
        tSealTimer(IN := FALSE);
        IF NOT bEnable THEN
            (* Reset command given by removing enable *)
            iState := 0;
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
``"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
