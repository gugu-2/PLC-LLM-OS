import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Automated Micro-Brewery Centrifuge Separation and Clarity Turbidity Control**

Task: Invent a highly complex, ultra-realistic control scenario for this domain. Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Brewery_Centrifuge\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Automated Micro-Brewery Centrifuge Separation and Clarity Turbidity Control

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_Brewery_Centrifuge
VAR_INPUT
    (* Required: at least 4-8 physical inputs with types and comments *)
    bEnable                 : BOOL;     (* System master enable signal from SCADA *)
    bEmergencyStop          : BOOL;     (* Safety circuit OK, active high - immediate shutdown on FALSE *)
    rTurbidityIn            : REAL;     (* Inlet turbidity measurement in EBC or NTU *)
    rFlowRateIn             : REAL;     (* Inlet flow rate in hL/h from magnetic flowmeter *)
    rBowlSpeedFeedback      : REAL;     (* Centrifuge bowl speed feedback in RPM *)
    rMotorTemp              : REAL;     (* Main drive motor temperature in DegC *)
    bDischargeReq           : BOOL;     (* Manual or upstream-requested solids discharge trigger *)
    bCIP_Mode               : BOOL;     (* Clean-in-place mode active signal from CIP sequencer *)
END_VAR
VAR_OUTPUT
    (* Required: at least 3-6 outputs with types and comments *)
    bSystemReady            : BOOL;     (* Centrifuge is running at setpoint speed and ready for product feed *)
    rTargetSpeedRPM         : REAL;     (* Speed setpoint output to VFD *)
    rFeedPumpControl        : REAL;     (* 0-100% control signal to product feed pump *)
    bDischargeValve         : BOOL;     (* Command to open solids discharge mechanism valve *)
    bAlarm                  : BOOL;     (* General fault alarm output for HMI/SCADA *)
    iFaultCode              : INT;      (* Diagnostics fault code for detailed troubleshooting *)
    rTurbidityOut           : REAL;     (* Filtered output turbidity signal for logging *)
END_VAR
VAR
    (* Internal state variables *)
    iState                  : INT := 0; (* Main State Machine Step *)
    rTurbidityFiltered      : REAL := 0.0; (* EMA filter for turbidity *)
    tStartupTimer           : TON;      (* Timer for bowl acceleration phase *)
    tDischargeTimer         : TON;      (* Timer for solids discharge sequence *)
    tCIPTimer               : TON;      (* Timer for CIP cycle duration limits *)
    
    (* Filter Constants *)
    ALPHA                   : REAL := 0.15; (* Exponential Moving Average weight *)
    
    (* Operational Constants *)
    MAX_RPM                 : REAL := 7500.0; (* Maximum allowed bowl speed *)
    NOMINAL_RPM             : REAL := 6800.0; (* Nominal processing bowl speed *)
    MAX_TEMP                : REAL := 85.0;   (* Motor temperature high-high limit *)
    TURBIDITY_LIMIT         : REAL := 50.0;   (* Target max turbidity; trigger for feed adjust or discharge *)
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety Interlocks and Hard Stops (Highest Priority) *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bAlarm := TRUE;
    iFaultCode := 99; (* Critical E-Stop active *)
    rTargetSpeedRPM := 0.0;
    rFeedPumpControl := 0.0;
    bDischargeValve := FALSE;
    iState := 0;
    RETURN;
END_IF;

IF rMotorTemp > MAX_TEMP THEN
    bAlarm := TRUE;
    iFaultCode := 10; (* Motor Overtemperature condition *)
    rTargetSpeedRPM := 0.0;
    rFeedPumpControl := 0.0;
    iState := 999; (* Transition to Fault State *)
END_IF;

(* 2. Signal Processing (EMA Filter for noisy Turbidity Sensor) *)
rTurbidityFiltered := (ALPHA * rTurbidityIn) + ((1.0 - ALPHA) * rTurbidityFiltered);
rTurbidityOut := rTurbidityFiltered;

(* 3. Main State Machine for Process Control *)
CASE iState OF
    0: (* IDLE & READY TO START *)
        bSystemReady := FALSE;
        rTargetSpeedRPM := 0.0;
        rFeedPumpControl := 0.0;
        bDischargeValve := FALSE;
        bAlarm := FALSE;
        iFaultCode := 0;
        
        IF bEnable AND NOT bCIP_Mode THEN
            iState := 10; (* Start Bowl Acceleration Phase *)
        ELSIF bEnable AND bCIP_Mode THEN
            iState := 100; (* Enter Clean-In-Place Mode *)
        END_IF;

    10: (* BOWL ACCELERATION *)
        rTargetSpeedRPM := NOMINAL_RPM;
        tStartupTimer(IN := TRUE, PT := T#120S); (* Allow 2 minutes for heavy bowl to spin up *)
        
        IF rBowlSpeedFeedback >= (NOMINAL_RPM * 0.95) THEN
            tStartupTimer(IN := FALSE);
            iState := 20; (* Transition to Nominal operation *)
        ELSIF tStartupTimer.Q THEN
            tStartupTimer(IN := FALSE);
            bAlarm := TRUE;
            iFaultCode := 12; (* Acceleration Timeout Fault *)
            iState := 999;
        END_IF;

    20: (* NOMINAL OPERATION - CLARITY CONTROL *)
        bSystemReady := TRUE;
        
        (* Cascade control pseudo-logic: modulate product feed pump based on measured turbidity *)
        IF rTurbidityFiltered > TURBIDITY_LIMIT THEN
            (* Slow down feed to increase residence time and improve clarity *)
            rFeedPumpControl := rFeedPumpControl - 1.0;
            IF rFeedPumpControl < 10.0 THEN
                rFeedPumpControl := 10.0; (* Minimum feed limit to prevent dead-heading *)
            END_IF;
        ELSE
            (* Safely increase feed if clarity is well within specs *)
            rFeedPumpControl := rFeedPumpControl + 0.5;
            IF rFeedPumpControl > 90.0 THEN
                rFeedPumpControl := 90.0; (* Maximum feed limit *)
            END_IF;
        END_IF;
        
        (* Automatic Discharge Trigger condition based on solids loading *)
        IF bDischargeReq OR (rTurbidityFiltered > (TURBIDITY_LIMIT * 1.5)) THEN
            iState := 30; (* Initiate Discharge Sequence *)
        END_IF;
        
        IF NOT bEnable THEN
            iState := 0; (* Normal Stop Requested *)
        END_IF;

    30: (* DISCHARGE SEQUENCE *)
        bSystemReady := FALSE;
        rFeedPumpControl := 0.0; (* Pause product feed during discharge *)
        bDischargeValve := TRUE; (* Open discharge mechanism briefly *)
        
        tDischargeTimer(IN := TRUE, PT := T#2S); (* Typical short open time for partial discharge *)
        IF tDischargeTimer.Q THEN
            bDischargeValve := FALSE;
            tDischargeTimer(IN := FALSE);
            iState := 20; (* Return to nominal operation and resume feed *)
        END_IF;

    100: (* CIP MODE *)
        bSystemReady := FALSE;
        rTargetSpeedRPM := 1500.0; (* Reduced speed for mechanical cleaning and rinsing *)
        rFeedPumpControl := 0.0;
        
        tCIPTimer(IN := TRUE, PT := T#30M); (* Max allowable CIP duration before auto-stop *)
        IF tCIPTimer.Q OR NOT bEnable THEN
            tCIPTimer(IN := FALSE);
            iState := 0;
        END_IF;
        
    999: (* FAULT HANDLING *)
        bSystemReady := FALSE;
        rTargetSpeedRPM := 0.0;
        rFeedPumpControl := 0.0;
        IF NOT bEnable THEN
            (* Reset fault state and return to idle if master enable is dropped *)
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
