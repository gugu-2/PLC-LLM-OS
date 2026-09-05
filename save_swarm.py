import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Utility-Scale Concentrating Solar Power (CSP) Molten Salt Receiver Tower**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Heliostat field optical flux map feed-forward, nitrate salt freezing prevention thermal tracing, and multi-zone receiver panel mass flow distribution). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_CSP_MoltenSaltTower\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Utility-Scale Concentrating Solar Power (CSP) Molten Salt Receiver Tower

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_CSP_MoltenSaltTowerControl
VAR_INPUT
    bSystemEnable           : BOOL;     (* Main enable for receiver tower control system *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal (E-Stop), TRUE = Healthy *)
    rInletSaltTemp          : REAL;     (* Cold salt inlet temperature [deg C] *)
    rReceiverPanelTemp      : REAL;     (* Average receiver panel surface temperature [deg C] *)
    rTargetOutletTemp       : REAL;     (* Desired hot salt outlet temperature [deg C] *)
    rHeliostatFluxFeedFwd   : REAL;     (* Anticipated thermal flux from heliostat field DNI tracking [MW/m2] *)
    rWindSpeed              : REAL;     (* Tower-top anemometer wind speed [m/s] *)
    bSaltFlowProven         : BOOL;     (* Flow meter verification of molten salt flow *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* System ready for full solar flux tracking *)
    rSaltPumpSpeedCmd       : REAL;     (* Variable frequency drive speed command for salt pump [0.0 - 100.0%] *)
    bHeatTracingEnable      : BOOL;     (* Enable electrical heat tracing to prevent salt freezing *)
    bDefocusCommand         : BOOL;     (* Emergency defocus command to heliostat field *)
    iOperatingState         : INT;      (* Current control state enum *)
    bAlarmHighTemp          : BOOL;     (* Receiver over-temperature alarm *)
    bAlarmFreezing          : BOOL;     (* Salt freezing risk alarm *)
END_VAR
VAR
    iState                  : INT := 0; (* Internal state machine variable *)
    tPreheatTimer           : TON;      (* Timer for electrical preheating *)
    tDefocusTimer           : TON;      (* Cooldown timer after defocus *)
    rFlowPID_Kp             : REAL := 2.5;
    rFlowPID_Ki             : REAL := 0.15;
    rFlowPID_Kd             : REAL := 0.05;
    rError                  : REAL;
    rLastError              : REAL;
    rIntegral               : REAL;
    rDerivative             : REAL;
    rMinPumpSpeed           : REAL := 25.0; (* Minimum safe flow to prevent hot spots *)
    rMaxPumpSpeed           : REAL := 100.0;
    rSaltFreezeTemp         : REAL := 290.0; (* Solar salt freezing point [deg C] *)
    rMaxPanelTemp           : REAL := 620.0; (* Max allowable panel metallurgical temperature [deg C] *)
    bLocalHeatTracing       : BOOL;
END_VAR

(* === SAFETY & INTERLOCK SUPERVISOR === *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bHeatTracingEnable := TRUE; (* Always ensure tracing is active on trip to avoid solidifying *)
    bDefocusCommand := TRUE;    (* Immediately remove solar flux *)
    rSaltPumpSpeedCmd := 0.0;
    iOperatingState := 99;      (* E-STOP state *)
    bAlarmHighTemp := FALSE;
    bAlarmFreezing := FALSE;
    RETURN;
END_IF;

(* === THERMAL SAFEGUARDS === *)
IF rReceiverPanelTemp > rMaxPanelTemp THEN
    bAlarmHighTemp := TRUE;
    bDefocusCommand := TRUE;
ELSE
    bAlarmHighTemp := FALSE;
    bDefocusCommand := FALSE;
END_IF;

IF rInletSaltTemp < (rSaltFreezeTemp + 15.0) THEN
    bAlarmFreezing := TRUE;
    bLocalHeatTracing := TRUE;
ELSE
    bAlarmFreezing := FALSE;
    bLocalHeatTracing := FALSE;
END_IF;
bHeatTracingEnable := bLocalHeatTracing;

(* === MAIN STATE MACHINE === *)
CASE iState OF
    0: (* IDLE & PRE-CHECK *)
        rSaltPumpSpeedCmd := 0.0;
        bSystemReady := FALSE;
        IF bSystemEnable AND (rInletSaltTemp >= rSaltFreezeTemp + 20.0) THEN
            iState := 10;
        END_IF;

    10: (* PRE-HEATING & TRACING VERIFICATION *)
        bLocalHeatTracing := TRUE;
        tPreheatTimer(IN := TRUE, PT := T#30S);
        IF tPreheatTimer.Q THEN
            tPreheatTimer(IN := FALSE);
            iState := 20;
        END_IF;
        IF NOT bSystemEnable THEN
            tPreheatTimer(IN := FALSE);
            iState := 0;
        END_IF;

    20: (* INITIAL FLOW ESTABLISHMENT *)
        rSaltPumpSpeedCmd := rMinPumpSpeed;
        IF bSaltFlowProven THEN
            iState := 30;
        END_IF;
        IF NOT bSystemEnable THEN
            iState := 0;
        END_IF;

    30: (* NORMAL OPERATION & PID CONTROL WITH FEEDFORWARD *)
        bSystemReady := TRUE;
        
        (* Calculate PID Error *)
        rError := rTargetOutletTemp - rReceiverPanelTemp;
        
        (* Integral Accumulation with Anti-Windup *)
        rIntegral := rIntegral + rError;
        IF rIntegral > 1000.0 THEN rIntegral := 1000.0; END_IF;
        IF rIntegral < -1000.0 THEN rIntegral := -1000.0; END_IF;
        
        (* Derivative *)
        rDerivative := rError - rLastError;
        rLastError := rError;
        
        (* Core PID Calculation - Note: Pump speed increases to COOL DOWN the receiver (more flow) *)
        rSaltPumpSpeedCmd := (rFlowPID_Kp * -rError) + (rFlowPID_Ki * -rIntegral) + (rFlowPID_Kd * -rDerivative);
        
        (* Add Feed-Forward based on incoming solar flux and wind cooling effect *)
        rSaltPumpSpeedCmd := rSaltPumpSpeedCmd + (rHeliostatFluxFeedFwd * 5.0) - (rWindSpeed * 0.5);
        
        (* Clamp Output *)
        IF rSaltPumpSpeedCmd < rMinPumpSpeed THEN
            rSaltPumpSpeedCmd := rMinPumpSpeed;
        ELSIF rSaltPumpSpeedCmd > rMaxPumpSpeed THEN
            rSaltPumpSpeedCmd := rMaxPumpSpeed;
        END_IF;
        
        (* Transitions *)
        IF NOT bSystemEnable OR bDefocusCommand THEN
            bSystemReady := FALSE;
            iState := 40;
        END_IF;

    40: (* CONTROLLED SHUTDOWN & DRAIN *)
        rSaltPumpSpeedCmd := rMinPumpSpeed; (* Maintain minimum flow while cooling *)
        tDefocusTimer(IN := TRUE, PT := T#120S);
        IF tDefocusTimer.Q THEN
            tDefocusTimer(IN := FALSE);
            rSaltPumpSpeedCmd := 0.0; (* Stop pump, allow gravity drain *)
            iState := 0;
        END_IF;
        
    99: (* FAULT / ESTOP *)
        (* Handled by top-level logic, wait for reset *)
        IF bEmergencyStop AND NOT bSystemEnable THEN
            iState := 0;
        END_IF;
END_CASE;

(* Update Output State *)
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
