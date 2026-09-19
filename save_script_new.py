import json, uuid, os

prompt = """<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: High-Volume Brewery Continuous Centrifuge Yeast Separation and Turbidity Interlock**

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
6. REPLY with: EVOLUTION COMPLETE: High-Volume Brewery Continuous Centrifuge Yeast Separation and Turbidity Interlock

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.
</USER_REQUEST>"""

code = """```iec-st
FUNCTION_BLOCK FB_Centrifuge_Yeast_Separation
VAR_INPUT
    bEnable                 : BOOL;     (* System overall enable signal *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal (Normally Closed = TRUE) *)
    rFeedFlowRate           : REAL;     (* Measured incoming feed flow rate (hL/h) *)
    rInletTurbidity         : REAL;     (* Inlet beer turbidity (EBC) *)
    rOutletTurbidity        : REAL;     (* Outlet beer turbidity (EBC) *)
    rBowlSpeedRPM           : REAL;     (* Actual centrifuge bowl speed (RPM) *)
    bVibrationHigh          : BOOL;     (* High vibration alarm sensor *)
    rTemperatureIn          : REAL;     (* Feed beer temperature (deg C) *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* Centrifuge ready for feed *)
    rFeedPumpSpeedRef       : REAL;     (* Speed reference to feed pump VFD (0-100%) *)
    bDischargeTrigger       : BOOL;     (* Signal to open yeast discharge mechanism *)
    bAlarm                  : BOOL;     (* Critical fault active *)
    iFaultCode              : INT;      (* Diagnostics fault code (0=None, 1=E-Stop, 2=Vibration, 3=Turbidity) *)
    rFilteredTurbidity      : REAL;     (* Noise-filtered outlet turbidity (EBC) *)
END_VAR
VAR
    iState                  : INT := 0; (* Internal state machine variable *)
    tStartupDelay           : TON;
    tDischargeTimer         : TON;
    tVibrationDebounce      : TON;
    rTurbidityBuffer        : ARRAY[0..4] OF REAL := [0.0, 0.0, 0.0, 0.0, 0.0];
    iBufferIndex            : INT := 0;
    rSumTurbidity           : REAL := 0.0;
    i                       : INT := 0;
    rPID_Kp                 : REAL := 1.2;
    rPID_Ki                 : REAL := 0.5;
    rError                  : REAL;
    rIntegral               : REAL := 0.0;
    rTargetTurbidity        : REAL := 1.5; (* Desired outlet EBC *)
    bDischargeActive        : BOOL := FALSE;
END_VAR

(* === MAIN SAFETY AND INTERLOCK LOGIC === *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bAlarm := TRUE;
    iFaultCode := 1;
    rFeedPumpSpeedRef := 0.0;
    bDischargeTrigger := FALSE;
    iState := 0;
    RETURN;
END_IF;

(* Vibration Debounce *)
tVibrationDebounce(IN := bVibrationHigh, PT := T#2S);
IF tVibrationDebounce.Q THEN
    bSystemReady := FALSE;
    bAlarm := TRUE;
    iFaultCode := 2;
    rFeedPumpSpeedRef := 0.0;
    iState := 0;
    RETURN;
END_IF;

(* Moving Average Filter for Outlet Turbidity *)
rTurbidityBuffer[iBufferIndex] := rOutletTurbidity;
iBufferIndex := (iBufferIndex + 1) MOD 5;
rSumTurbidity := 0.0;
FOR i := 0 TO 4 DO
    rSumTurbidity := rSumTurbidity + rTurbidityBuffer[i];
END_FOR;
rFilteredTurbidity := rSumTurbidity / 5.0;

(* Extreme High Turbidity Interlock *)
IF rFilteredTurbidity > 10.0 THEN
    bAlarm := TRUE;
    iFaultCode := 3;
    rFeedPumpSpeedRef := 0.0; (* Stop feeding immediately *)
    iState := 0; (* Force state to IDLE *)
    RETURN;
END_IF;

(* Normal operation state machine *)
CASE iState OF
    0: (* IDLE *)
        bSystemReady := FALSE;
        rFeedPumpSpeedRef := 0.0;
        bDischargeTrigger := FALSE;
        rIntegral := 0.0;
        IF bEnable AND NOT bAlarm THEN
            iState := 10;
        END_IF;

    10: (* RAMPING SPEED *)
        IF rBowlSpeedRPM > 6500.0 THEN (* Target operational speed *)
            tStartupDelay(IN := TRUE, PT := T#5S);
            IF tStartupDelay.Q THEN
                tStartupDelay(IN := FALSE);
                iState := 20;
            END_IF;
        END_IF;

    20: (* RUNNING & PID CONTROL *)
        bSystemReady := TRUE;
        bAlarm := FALSE;
        iFaultCode := 0;
        
        (* Calculate PID for Feed Pump Speed based on Turbidity Error *)
        rError := rTargetTurbidity - rFilteredTurbidity;
        rIntegral := rIntegral + (rError * 0.1); (* Assuming 100ms cycle time approx *)
        
        (* Anti-windup *)
        IF rIntegral > 50.0 THEN rIntegral := 50.0; END_IF;
        IF rIntegral < -50.0 THEN rIntegral := -50.0; END_IF;
        
        rFeedPumpSpeedRef := 50.0 + (rPID_Kp * rError) + (rPID_Ki * rIntegral);
        
        (* Clamp Output *)
        IF rFeedPumpSpeedRef > 100.0 THEN rFeedPumpSpeedRef := 100.0; END_IF;
        IF rFeedPumpSpeedRef < 20.0 THEN rFeedPumpSpeedRef := 20.0; END_IF;
        
        (* Automatic Discharge Trigger based on Feed Volume and Turbidity *)
        IF (rInletTurbidity > 50.0) AND (rFilteredTurbidity > 2.0) THEN
            iState := 30;
        END_IF;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    30: (* YEAST DISCHARGE SEQUENCE *)
        bDischargeTrigger := TRUE;
        tDischargeTimer(IN := TRUE, PT := T#2S);
        IF tDischargeTimer.Q THEN
            tDischargeTimer(IN := FALSE);
            bDischargeTrigger := FALSE;
            iState := 20; (* Return to running *)
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}

with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
