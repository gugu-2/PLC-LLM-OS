import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Commercial Airport Automated Baggage Handling System (BHS) High-Speed Cross-Belt Sorter**

Task: Invent a highly complex, ultra-realistic control scenario for this domain. Make this code EVEN BETTER, MORE ADVANCED, and MORE RIGOROUS than previous iterations. Include extreme edge-case handling, advanced math, and robust fault-tolerance.

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
   code = \"\"\"```iec-st\nFUNCTION_BLOCK FB_AirportBHS_CrossBelt\n//...\nEND_FUNCTION_BLOCK\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Commercial Airport Automated Baggage Handling System (BHS) High-Speed Cross-Belt Sorter

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_BHS_CrossBeltSorter
VAR_INPUT
    bEnable           : BOOL;     (* System master enable *)
    bEmergencyStop    : BOOL;     (* E-Stop safety circuit status (TRUE = OK) *)
    bInductionDetect  : BOOL;     (* Photo-eye detecting bag induction *)
    rBagWeight_kg     : REAL;     (* Bag weight from scale in kg *)
    rMainLineSpeed    : REAL;     (* Main sorter line speed in m/s *)
    bDestAvailable    : BOOL;     (* Destination chute availability *)
    bEncoderSync      : BOOL;     (* High-speed encoder sync pulse *)
    iTargetChute      : INT;      (* Target chute ID for induction *)
END_VAR
VAR_OUTPUT
    bSystemReady      : BOOL;     (* Sorter is ready for induction *)
    rBeltDischargeSpd : REAL;     (* Calculated discharge cross-belt speed (m/s) *)
    bDischargeTrigger : BOOL;     (* Trigger for cross-belt discharge action *)
    bAlarm            : BOOL;     (* General fault alarm *)
    iErrorCode        : INT;      (* Specific error code for diagnostics *)
    rFilteredWeight   : REAL;     (* Exponential moving average of weight *)
END_VAR
VAR
    iState            : INT := 0; (* Main state machine step *)
    tEStopTimer       : TON;
    tDischargeWindow  : TON;
    rWeightBuffer     : ARRAY[0..9] OF REAL;
    iBufferIdx        : INT := 0;
    rWeightSum        : REAL := 0.0;
    bBagInTransit     : BOOL := FALSE;
    rCalculatedDelay  : REAL;
    bInductionEdge    : R_TRIG;
END_VAR

(* === SAFETY AND INTERLOCKS === *)
IF NOT bEmergencyStop THEN
    iState := 999; (* FAULT STATE *)
    bSystemReady := FALSE;
    bDischargeTrigger := FALSE;
    rBeltDischargeSpd := 0.0;
    bAlarm := TRUE;
    iErrorCode := 1001; (* E-Stop Pressed *)
    RETURN;
END_IF;

(* Edge detection for induction *)
bInductionEdge(CLK := bInductionDetect);

(* === SENSOR NOISE FILTERING (Moving Average) === *)
IF bInductionEdge.Q THEN
    rWeightSum := rWeightSum - rWeightBuffer[iBufferIdx] + rBagWeight_kg;
    rWeightBuffer[iBufferIdx] := rBagWeight_kg;
    rFilteredWeight := rWeightSum / 10.0;
    iBufferIdx := (iBufferIdx + 1) MOD 10;
END_IF;

(* === MAIN CONTROL STATE MACHINE === *)
CASE iState OF
    0: (* INIT *)
        bSystemReady := FALSE;
        bAlarm := FALSE;
        iErrorCode := 0;
        IF bEnable AND bEmergencyStop THEN
            iState := 10;
        END_IF;

    10: (* IDLE & SYNCHRONIZING *)
        bSystemReady := TRUE;
        bDischargeTrigger := FALSE;
        rBeltDischargeSpd := 0.0;
        IF bInductionEdge.Q THEN
            bBagInTransit := TRUE;
            iState := 20;
        END_IF;
        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    20: (* TRACKING & KINEMATIC CALCULATION *)
        bSystemReady := FALSE; (* Busy processing bag *)
        
        (* Calculate exact discharge speed based on weight and main line speed *)
        (* Heavier bags require higher discharge coefficient to overcome inertia *)
        IF rFilteredWeight > 35.0 THEN
            iState := 999; (* OOG: Out of gauge, bag too heavy *)
            iErrorCode := 2001;
        ELSE
            rBeltDischargeSpd := rMainLineSpeed * (1.0 + (rFilteredWeight * 0.015));
            iState := 30;
        END_IF;

    30: (* AWAITING DISCHARGE WINDOW *)
        IF bDestAvailable AND bEncoderSync THEN
            bDischargeTrigger := TRUE;
            tDischargeWindow(IN := TRUE, PT := T#2S);
            IF tDischargeWindow.Q THEN
                iState := 40;
            END_IF;
        ELSIF NOT bDestAvailable THEN
            iState := 999; (* Missed sort *)
            iErrorCode := 3001;
        END_IF;

    40: (* DISCHARGE COMPLETE *)
        bDischargeTrigger := FALSE;
        bBagInTransit := FALSE;
        tDischargeWindow(IN := FALSE);
        iState := 10;

    999: (* FAULT HANDLING *)
        bSystemReady := FALSE;
        bAlarm := TRUE;
        bDischargeTrigger := FALSE;
        rBeltDischargeSpd := 0.0;
        IF NOT bEnable THEN
            (* Require disable to clear non-estop faults *)
            iState := 0;
        END_IF;

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
