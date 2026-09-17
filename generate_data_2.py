import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial Metal Forging Hydraulic Press Multi-Stage Die Pressure and Billet Temperature**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_ForgingPress_Control\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Metal Forging Hydraulic Press Multi-Stage Die Pressure and Billet Temperature

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.
"""

code = """```iec-st
FUNCTION_BLOCK FB_ForgingPress_Control
VAR_INPUT
    bSystemEnable       : BOOL;     (* Main safety interlocking enable signal *)
    bEStopOK            : BOOL;     (* Emergency stop circuit OK signal *)
    rBilletTempIR       : REAL;     (* Infrared sensor reading of billet temp (deg C) *)
    rDiePressure        : REAL;     (* Current hydraulic die pressure (bar) *)
    bPositionSensTop    : BOOL;     (* Ram at Top Dead Center (TDC) *)
    bPositionSensBot    : BOOL;     (* Ram at Bottom Dead Center (BDC) *)
    bManualOverride     : BOOL;     (* Manual control mode selector *)
    rSetPressureLimit   : REAL;     (* Target pressure limit for the cycle (bar) *)
END_VAR
VAR_OUTPUT
    bHydraulicPumpOn    : BOOL;     (* Command to start main hydraulic pump *)
    rProportionalValve  : REAL;     (* 0.0 - 100.0% signal to main servo-proportional valve *)
    bHeaterControl      : BOOL;     (* Command to activate die heating elements *)
    bCycleComplete      : BOOL;     (* Indicates one complete forging cycle finished *)
    bAlarmFault         : BOOL;     (* General fault alarm (e.g. pressure too high, temp too low) *)
    iFaultCode          : INT;      (* Specific fault code for HMI display *)
END_VAR
VAR
    iState              : INT := 0; 
    tPreHeatTimer       : TON;
    tDwellTimer         : TON;
    tWatchdogTimer      : TON;
    rFilteredTemp       : REAL;     (* Exponential moving average filter for temperature *)
    rFilteredPressure   : REAL;     (* Filtered pressure signal *)
    rIntegralError      : REAL := 0.0;
    rPrevError          : REAL := 0.0;
    rDerivative         : REAL := 0.0;
    rError              : REAL := 0.0;
    rKp                 : REAL := 2.5;
    rKi                 : REAL := 0.1;
    rKd                 : REAL := 0.5;
END_VAR

(* === SAFETY & SENSOR FILTERING === *)
IF NOT bEStopOK THEN
    iState := 999; (* EMERGENCY STOP STATE *)
    bHydraulicPumpOn := FALSE;
    rProportionalValve := 0.0;
    bHeaterControl := FALSE;
    bAlarmFault := TRUE;
    iFaultCode := 101; (* E-Stop Pressed *)
    RETURN;
END_IF;

(* Exponential Moving Average filter for noisy IR temperature sensor *)
rFilteredTemp := rFilteredTemp * 0.9 + rBilletTempIR * 0.1;

(* Filtering for hydraulic pressure spikes *)
rFilteredPressure := rFilteredPressure * 0.8 + rDiePressure * 0.2;

(* Watchdog timer for overall machine health during cycle *)
tWatchdogTimer(IN := (iState > 0 AND iState < 999), PT := T#45S);
IF tWatchdogTimer.Q THEN
    iState := 999; 
    bAlarmFault := TRUE;
    iFaultCode := 102; (* Cycle timeout fault *)
END_IF;

(* === MAIN STATE MACHINE === *)
CASE iState OF
    0: (* IDLE - WAIT FOR ENABLE AND TOP POSITION *)
        bHydraulicPumpOn := FALSE;
        rProportionalValve := 0.0;
        bHeaterControl := FALSE;
        bCycleComplete := FALSE;
        bAlarmFault := FALSE;
        iFaultCode := 0;
        
        IF bSystemEnable AND bPositionSensTop AND NOT bManualOverride THEN
            iState := 10;
        END_IF;

    10: (* PRE-HEAT DIE & BILLET TEMP CHECK *)
        bHydraulicPumpOn := TRUE;
        bHeaterControl := TRUE;
        rProportionalValve := 5.0; (* Keep ram steady *)
        
        tPreHeatTimer(IN := TRUE, PT := T#10S);
        IF tPreHeatTimer.Q THEN
            tPreHeatTimer(IN := FALSE);
            IF rFilteredTemp >= 1150.0 AND rFilteredTemp <= 1250.0 THEN
                iState := 20; (* Temp OK, proceed to approach *)
            ELSE
                iState := 999;
                bAlarmFault := TRUE;
                iFaultCode := 201; (* Billet temperature out of optimal forging bounds *)
            END_IF;
        END_IF;

    20: (* FAST APPROACH *)
        bHeaterControl := FALSE;
        rProportionalValve := 80.0; (* Fast downward movement *)
        
        IF rFilteredPressure > 50.0 THEN (* Contact with billet detected *)
            iState := 30;
        END_IF;

    30: (* PRESSING & PRESSURE PID CONTROL *)
        (* PID calculations for proportional valve to achieve target pressure *)
        rError := rSetPressureLimit - rFilteredPressure;
        rIntegralError := rIntegralError + (rError * 0.1); (* 100ms assumed scan rate *)
        rDerivative := (rError - rPrevError) / 0.1;
        rPrevError := rError;
        
        rProportionalValve := (rKp * rError) + (rKi * rIntegralError) + (rKd * rDerivative);
        
        (* Clamp valve output *)
        IF rProportionalValve > 100.0 THEN rProportionalValve := 100.0; END_IF;
        IF rProportionalValve < 10.0 THEN rProportionalValve := 10.0; END_IF;
        
        IF rFilteredPressure >= (rSetPressureLimit * 0.98) THEN
            iState := 40;
        END_IF;

    40: (* DWELL / HOLD PRESSURE *)
        rProportionalValve := 50.0; (* Holding valve position roughly center *)
        tDwellTimer(IN := TRUE, PT := T#2S);
        IF tDwellTimer.Q THEN
            tDwellTimer(IN := FALSE);
            iState := 50;
        END_IF;

    50: (* RETRACT *)
        rProportionalValve := -75.0; (* Fast upward movement, negative denotes retract in this valve logic *)
        IF bPositionSensTop THEN
            rProportionalValve := 0.0;
            bCycleComplete := TRUE;
            iState := 60;
        END_IF;

    60: (* CYCLE END / WAIT FOR DISABLE *)
        IF NOT bSystemEnable THEN
            bCycleComplete := FALSE;
            iState := 0;
        END_IF;

    999: (* FAULT HANDLING *)
        bHydraulicPumpOn := FALSE;
        rProportionalValve := 0.0;
        bHeaterControl := FALSE;
        
        IF NOT bAlarmFault THEN (* Fault reset triggered externally via fault clearing bAlarmFault *)
            iState := 0;
            tPreHeatTimer(IN := FALSE);
            tDwellTimer(IN := FALSE);
            tWatchdogTimer(IN := FALSE);
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump({"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}, f, ensure_ascii=False)
print(f"Saved to {filename}")
