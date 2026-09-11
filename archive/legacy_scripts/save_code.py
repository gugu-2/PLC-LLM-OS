import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Next-Gen Subsea Carbon Capture and Storage (CCS) Liquid CO2 Injection Tree**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Supercritical CO2 hydrate phase-envelope avoidance, Joule-Thomson effect cryogenic throttling mitigation, and formation-fracture acoustic emission tracking). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_SubseaCCS_InjectionTree\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Next-Gen Subsea Carbon Capture and Storage (CCS) Liquid CO2 Injection Tree

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_SubseaCCS_InjectionTree
(* 
   =============================================================================
   Elite Automation Architecture
   Domain: Next-Gen Subsea Carbon Capture and Storage (CCS) Liquid CO2 Injection Tree
   Purpose: Supercritical CO2 hydrate phase-envelope avoidance, Joule-Thomson effect 
            cryogenic throttling mitigation, and formation-fracture acoustic emission tracking.
   =============================================================================
*)
VAR_INPUT
    bEnable                 : BOOL;     (* System Enable Signal - Watchdog verified *)
    bSafetyShutdown         : BOOL;     (* Main Subsea Safety Interlock (SIL-3) *)
    rP_Wellhead             : REAL;     (* Wellhead Pressure (Bar) *)
    rT_Wellhead             : REAL;     (* Wellhead Temperature (Deg C) *)
    rFlowRate               : REAL;     (* CO2 Mass Flow Rate (kg/s) *)
    rAcousticEmission       : REAL;     (* Formation fracture proxy sensor (mV) *)
    rChokePositionFeedback  : REAL;     (* Choke valve position (0-100%) *)
    rJouleThomsonLimit      : REAL;     (* Minimum allowable temp post-choke (Deg C) *)
END_VAR

VAR_OUTPUT
    bSystemReady            : BOOL;     (* System is stable and ready for injection *)
    rChokeCommand           : REAL;     (* Directed position to the injection choke valve (0-100%) *)
    bHydrateWarning         : BOOL;     (* Pre-alarm for hydrate formation risk *)
    bFractureAlarm          : BOOL;     (* Alarm for acoustic emission exceeding limits *)
    bEmergencyClose         : BOOL;     (* Command to close safety valves immediately *)
END_VAR

VAR
    (* Internal State and Filtering *)
    iState                  : INT := 0; (* Main State Machine *)
    rFilteredT              : REAL;     (* First-order low pass filtered Temperature *)
    rFilteredP              : REAL;     (* First-order low pass filtered Pressure *)
    tStartupDelay           : TON;
    tSettleDelay            : TON;
    tSafetyTimer            : TON;
    
    (* Phase Envelope Constants *)
    C_HYDRATE_T_MARGIN      : REAL := 2.5;  (* Safety margin above hydrate curve *)
    C_HYDRATE_P_COEFF       : REAL := 0.08; (* Simplified empirical coefficient for hydrate boundary *)
    rHydrateThresholdT      : REAL;         (* Calculated threshold *)
    
    (* Control Loop *)
    rErrorP                 : REAL;
    rIntegral               : REAL := 0.0;
    Kp                      : REAL := 1.2;
    Ki                      : REAL := 0.05;
    rTargetP                : REAL := 150.0; (* 150 Bar supercritical injection target *)
END_VAR

(* === MAIN SAFETY INTERLOCK === *)
IF NOT bSafetyShutdown OR NOT bEnable THEN
    bSystemReady := FALSE;
    rChokeCommand := 0.0;
    bHydrateWarning := FALSE;
    bFractureAlarm := FALSE;
    bEmergencyClose := TRUE;
    iState := 0;
    rIntegral := 0.0;
    RETURN;
END_IF;

bEmergencyClose := FALSE;

(* === SENSOR FILTERING (First-order LPF) === *)
(* Assuming a generic cycle time of 100ms for tau calculation *)
rFilteredT := rFilteredT + 0.1 * (rT_Wellhead - rFilteredT);
rFilteredP := rFilteredP + 0.1 * (rP_Wellhead - rFilteredP);

(* === FORMATION FRACTURE MONITORING === *)
IF rAcousticEmission > 850.0 THEN
    bFractureAlarm := TRUE;
ELSE
    bFractureAlarm := FALSE;
END_IF;

(* === PHASE ENVELOPE / HYDRATE AVOIDANCE === *)
(* Simple empirical check for supercritical CO2 hydrate envelope *)
rHydrateThresholdT := (rFilteredP * C_HYDRATE_P_COEFF) + C_HYDRATE_T_MARGIN;
IF rFilteredT < rHydrateThresholdT OR rFilteredT < rJouleThomsonLimit THEN
    bHydrateWarning := TRUE;
ELSE
    bHydrateWarning := FALSE;
END_IF;

(* === STATE MACHINE FOR CHOKE CONTROL === *)
CASE iState OF
    0: (* INITIALIZATION / IDLE *)
        bSystemReady := FALSE;
        rChokeCommand := 0.0;
        IF bEnable AND bSafetyShutdown THEN
            tStartupDelay(IN := TRUE, PT := T#10S);
            IF tStartupDelay.Q THEN
                tStartupDelay(IN := FALSE);
                iState := 10;
            END_IF;
        ELSE
            tStartupDelay(IN := FALSE);
        END_IF;

    10: (* PRESSURE EQUALIZATION *)
        (* Slowly crack the choke valve to prevent extreme J-T cooling *)
        rChokeCommand := 5.0; 
        tSettleDelay(IN := TRUE, PT := T#30S);
        IF tSettleDelay.Q THEN
            tSettleDelay(IN := FALSE);
            IF NOT bHydrateWarning THEN
                iState := 20;
            END_IF;
        END_IF;

    20: (* ACTIVE INJECTION CONTROL (PID) *)
        bSystemReady := TRUE;
        
        (* Supercritical Pressure Control Loop *)
        rErrorP := rTargetP - rFilteredP;
        
        (* Anti-windup *)
        IF (rChokeCommand < 100.0 AND rErrorP > 0.0) OR (rChokeCommand > 0.0 AND rErrorP < 0.0) THEN
            rIntegral := rIntegral + (rErrorP * Ki);
        END_IF;
        
        rChokeCommand := (rErrorP * Kp) + rIntegral;
        
        (* Clamp Output *)
        IF rChokeCommand > 100.0 THEN rChokeCommand := 100.0; END_IF;
        IF rChokeCommand < 5.0 THEN rChokeCommand := 5.0; END_IF;

        (* Failsafe fall-back if temperature drops too fast *)
        IF bHydrateWarning THEN
            iState := 30; (* J-T Mitigation *)
        END_IF;
        
    30: (* J-T MITIGATION HOLD *)
        (* Hold choke steady, stop integral windup, wait for temp to recover *)
        bSystemReady := FALSE;
        tSafetyTimer(IN := TRUE, PT := T#60S);
        IF NOT bHydrateWarning THEN
            tSafetyTimer(IN := FALSE);
            iState := 20;
        END_IF;
        
        (* If it doesn't recover, shutdown *)
        IF tSafetyTimer.Q THEN
            tSafetyTimer(IN := FALSE);
            bEmergencyClose := TRUE;
            iState := 0;
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
