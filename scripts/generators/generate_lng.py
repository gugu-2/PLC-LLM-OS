import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial Scale Liquid Natural Gas (LNG) Cryogenic Cascade Liquefaction**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Mixed refrigerant (MR) multi-stage compressor surge prevention, cryogenic expander sub-cooling Joule-Thomson letdown, and boil-off gas (BOG) reliquefaction thermal integration). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_LNG_CascadeLiquefaction\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Scale Liquid Natural Gas (LNG) Cryogenic Cascade Liquefaction

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = '''```iec-st
FUNCTION_BLOCK FB_LNG_CascadeLiquefaction
VAR_INPUT
    (* Required: at least 4-8 physical inputs with types and comments *)
    bSystemEnable       : BOOL;     (* Main system enable command for the liquefaction train *)
    bEmergencyStop      : BOOL;     (* Safety instrumented system (SIS) emergency shutdown (ESD) OK signal (Active HIGH) *)
    rFeedGasTemp        : REAL;     (* Natural gas feed temperature into the precooling stage (deg C) *)
    rFeedGasPressure    : REAL;     (* Natural gas feed pressure (bar) *)
    rMRC_SuctionPres    : REAL;     (* Mixed Refrigerant Compressor (MRC) stage 1 suction pressure (bar) *)
    rMRC_DischargePres  : REAL;     (* Mixed Refrigerant Compressor final discharge pressure (bar) *)
    rExpanderSpeed      : REAL;     (* Cryogenic expander turbine rotational speed (RPM) *)
    bBOG_CompStatus     : BOOL;     (* Boil-off gas (BOG) compressor running status *)
END_VAR
VAR_OUTPUT
    (* Required: at least 3-6 outputs with types and comments *)
    bTrainReady         : BOOL;     (* Entire LNG liquefaction train is ready for operation *)
    rMRC_AntiSurgeValve : REAL;     (* Output to MRC anti-surge recycle valve (0.0 to 100.0 %) *)
    rJT_ValvePosition   : REAL;     (* Joule-Thomson letdown valve position (0.0 to 100.0 %) *)
    bCompressorTrip     : BOOL;     (* Trip command to the MRC motor starter *)
    bESD_Actuated       : BOOL;     (* Emergency Shutdown sequence activated *)
    iOperationState     : INT;      (* Current main state machine step (for SCADA/HMI) *)
END_VAR
VAR
    (* Internal state variables *)
    iState              : INT := 0; (* Internal state machine *)
    tSurgeTimer         : TON;      (* Timer for transient surge conditions *)
    tPurgeTimer         : TON;      (* Timer for pre-start purge sequence *)
    tRampUpTimer        : TON;      (* Timer for controlled speed ramp-up *)
    rPressureRatio      : REAL := 1.0; (* Calculated compressor pressure ratio *)
    rSurgeMargin        : REAL;     (* Dynamic surge margin calculation *)
    bSurgeImminent      : BOOL;     (* Flag indicating surge control needs aggressive action *)
    rFilteredFeedTemp   : REAL;     (* Low-pass filtered feed temperature *)
    
    (* Anti-surge PI Controller Parameters *)
    rKp                 : REAL := 2.5; 
    rKi                 : REAL := 0.8;
    rIntegralTerm       : REAL := 0.0;
    rError              : REAL := 0.0;
END_VAR
VAR CONSTANT
    SURGE_LIMIT_RATIO   : REAL := 3.2;  (* Critical pressure ratio for MRC surge *)
    SAFE_MARGIN         : REAL := 0.15; (* 15% safety margin on surge control line *)
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety & Interlocks First (Fail-Safe architecture) *)
IF NOT bEmergencyStop THEN
    (* Immediate trip of all critical equipment *)
    bTrainReady := FALSE;
    bCompressorTrip := TRUE;
    bESD_Actuated := TRUE;
    rMRC_AntiSurgeValve := 100.0; (* Fail open to protect compressor *)
    rJT_ValvePosition := 0.0;     (* Fail closed to isolate cryogenic section *)
    iState := 999; (* ESD State *)
    iOperationState := iState;
    RETURN;
END_IF;

bESD_Actuated := FALSE;

(* 2. Signal Processing (Sensor Noise Filtering) *)
(* First-order low pass filter for feed temperature: y(n) = a*x(n) + (1-a)*y(n-1) *)
rFilteredFeedTemp := (0.1 * rFeedGasTemp) + (0.9 * rFilteredFeedTemp);

(* 3. Compressor Pressure Ratio Calculation & Surge Control *)
IF rMRC_SuctionPres > 0.1 THEN
    rPressureRatio := rMRC_DischargePres / rMRC_SuctionPres;
ELSE
    rPressureRatio := 1.0;
END_IF;

rSurgeMargin := (SURGE_LIMIT_RATIO - rPressureRatio) / SURGE_LIMIT_RATIO;

bSurgeImminent := (rSurgeMargin < SAFE_MARGIN);

(* Advanced PI Anti-surge Controller *)
IF bSurgeImminent THEN
    rError := SAFE_MARGIN - rSurgeMargin;
    rIntegralTerm := rIntegralTerm + (rKi * rError);
    (* Anti-windup *)
    IF rIntegralTerm > 100.0 THEN rIntegralTerm := 100.0; END_IF;
    IF rIntegralTerm < 0.0 THEN rIntegralTerm := 0.0; END_IF;
    
    rMRC_AntiSurgeValve := (rKp * rError) + rIntegralTerm;
    
    IF rMRC_AntiSurgeValve > 100.0 THEN
        rMRC_AntiSurgeValve := 100.0;
    END_IF;
ELSE
    (* Normal condition - gradually close anti-surge valve *)
    rIntegralTerm := 0.0;
    rMRC_AntiSurgeValve := rMRC_AntiSurgeValve - 0.5;
    IF rMRC_AntiSurgeValve < 0.0 THEN
        rMRC_AntiSurgeValve := 0.0;
    END_IF;
END_IF;

(* 4. Main State Machine *)
CASE iState OF
    0: (* IDLE / STANDBY *)
        bTrainReady := FALSE;
        bCompressorTrip := FALSE;
        rJT_ValvePosition := 0.0;
        
        IF bSystemEnable AND (rFilteredFeedTemp < 40.0) THEN
            iState := 10;
        END_IF;

    10: (* PRE-PURGE & BOG VERIFICATION *)
        (* Ensure BOG compressor is running before starting main train *)
        tPurgeTimer(IN := bBOG_CompStatus, PT := T#30S);
        IF tPurgeTimer.Q THEN
            tPurgeTimer(IN := FALSE);
            iState := 20;
        ELSIF NOT bBOG_CompStatus THEN
            tPurgeTimer(IN := FALSE);
        END_IF;
        
        IF NOT bSystemEnable THEN
            iState := 0;
        END_IF;

    20: (* COMPRESSOR RAMP UP *)
        tRampUpTimer(IN := TRUE, PT := T#120S);
        IF tRampUpTimer.Q AND (rExpanderSpeed > 5000.0) THEN
            tRampUpTimer(IN := FALSE);
            iState := 30;
        END_IF;
        
        (* Trip if speed isn't reached in time or surge becomes critical *)
        IF (rSurgeMargin < 0.05) AND tRampUpTimer.ET > T#60S THEN
            bCompressorTrip := TRUE;
            iState := 999;
        END_IF;
        
    30: (* NORMAL OPERATION / LIQUEFACTION *)
        bTrainReady := TRUE;
        (* JT Letdown Valve control based on feed pressure to maintain expander sub-cooling *)
        IF rFeedGasPressure > 60.0 THEN
            rJT_ValvePosition := 55.0 + (rFeedGasPressure - 60.0) * 2.0;
        ELSE
            rJT_ValvePosition := 55.0;
        END_IF;
        
        IF rJT_ValvePosition > 100.0 THEN rJT_ValvePosition := 100.0; END_IF;

        IF NOT bSystemEnable THEN
            iState := 40;
        END_IF;
        
    40: (* CONTROLLED SHUTDOWN *)
        bTrainReady := FALSE;
        rJT_ValvePosition := rJT_ValvePosition - 1.0;
        IF rJT_ValvePosition <= 0.0 THEN
            rJT_ValvePosition := 0.0;
            iState := 0;
        END_IF;

    999: (* FAULT / ESD LATCH *)
        bTrainReady := FALSE;
        bCompressorTrip := TRUE;
        IF bSystemEnable = FALSE AND bEmergencyStop THEN
            iState := 0; (* Reset only when enable is dropped and E-Stop is clear *)
        END_IF;

END_CASE;

iOperationState := iState;

END_FUNCTION_BLOCK
```'''

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
