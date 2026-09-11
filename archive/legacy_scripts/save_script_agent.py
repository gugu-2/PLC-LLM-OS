import json, uuid
import os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Advanced Glass Fiber Stranding and Pultrusion Line**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 10,000-end creel tension dynamic decoupling, radio-frequency (RF) dielectric heating curing, and caterpillar puller traction slip compensation). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_FiberPultrusion\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Advanced Glass Fiber Stranding and Pultrusion Line

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.
</USER_REQUEST>"""

code = """```iec-st
FUNCTION_BLOCK FB_PultrusionLine_AdvControl
VAR_INPUT
    (* Physical system enablement and safety *)
    bSystemEnable           : BOOL;     (* Main line operation enable *)
    bEStop_OK               : BOOL;     (* Safety circuit loop intact and OK *)
    bRF_Heater_Ready        : BOOL;     (* RF dielectric heater is powered and ready *)
    
    (* Process measurements *)
    rCreelTension_Avg       : REAL;     (* Average tension across the 10,000-end creel (N) *)
    rPullerSpeed_Act        : REAL;     (* Actual caterpillar puller speed (m/s) from encoder *)
    rDieTemp_Act            : REAL;     (* Die temperature actual value (deg C) *)
    rResinViscosity         : REAL;     (* Impregnation bath resin viscosity (Pa.s) *)
    rLineTension_Exit       : REAL;     (* Final product tension at exit (N) *)
END_VAR

VAR_OUTPUT
    (* Actuator references and controls *)
    bSystemReady            : BOOL;     (* Pultrusion line is ready for operation *)
    rCreelTension_Ref       : REAL;     (* Tension reference for individual creel brakes (N) *)
    rPullerSpeed_Ref        : REAL;     (* Reference speed to puller VFD (m/s) *)
    rRF_Power_Ref           : REAL;     (* Reference power to RF curing heater (kW) *)
    
    (* Status and Alarms *)
    bTensionSlipAlarm       : BOOL;     (* Puller slip or tension imbalance detected *)
    bCureTempAlarm          : BOOL;     (* Curing temperature out of tolerance limits *)
    iOperatingState         : INT;      (* Current internal state machine value *)
END_VAR

VAR
    (* Internal state tracking and timers *)
    iState                  : INT := 0; 
    tStartupDelay           : TON;
    tTensionSettleTimer     : TON;
    tSlipDetectTimer        : TON;
    
    (* Filtering and control loop variables *)
    rFilteredTension        : REAL := 0.0;
    rTensionError           : REAL := 0.0;
    rTensionIntegral        : REAL := 0.0;
    rIntegralGain           : REAL := 0.05;
    rProportionalGain       : REAL := 1.25;
    
    (* Slip compensation logic *)
    rExpectedTension        : REAL := 0.0;
    rSlipThreshold          : REAL := 250.0; (* N *)
END_VAR

(* === MAIN LOGIC === *)

(* Safety and Enable Interlock Check *)
IF NOT bEStop_OK THEN
    bSystemReady := FALSE;
    rCreelTension_Ref := 0.0;
    rPullerSpeed_Ref := 0.0;
    rRF_Power_Ref := 0.0;
    bTensionSlipAlarm := FALSE;
    bCureTempAlarm := FALSE;
    iState := 0;
    iOperatingState := iState;
    RETURN;
END_IF;

(* State Machine for Line Sequencing *)
CASE iState OF
    0: (* IDLE & SAFETY VERIFICATION *)
        bSystemReady := FALSE;
        rPullerSpeed_Ref := 0.0;
        rRF_Power_Ref := 0.0;
        IF bSystemEnable AND bRF_Heater_Ready THEN
            iState := 10;
        END_IF;
        
    10: (* PRE-TENSIONING THE CREEL *)
        (* Slowly apply tension to avoid snapping delicate glass fibers *)
        bSystemReady := TRUE;
        rCreelTension_Ref := 50.0; (* Starting base tension (N) *)
        tTensionSettleTimer(IN := TRUE, PT := T#10S);
        
        IF tTensionSettleTimer.Q THEN
            tTensionSettleTimer(IN := FALSE);
            iState := 20;
        END_IF;
        
    20: (* RAMP TO PRODUCTION SPEED & PID TENSION CONTROL *)
        (* Calculate dynamic decoupling tension control using PI algorithm *)
        rFilteredTension := (rFilteredTension * 0.9) + (rCreelTension_Avg * 0.1);
        rTensionError := 500.0 - rFilteredTension; (* Target tension is 500 N *)
        
        (* Anti-windup integration *)
        IF rTensionIntegral < 1000.0 AND rTensionIntegral > -1000.0 THEN
            rTensionIntegral := rTensionIntegral + (rTensionError * rIntegralGain);
        END_IF;
        
        rCreelTension_Ref := 500.0 + (rTensionError * rProportionalGain) + rTensionIntegral;
        
        (* Ramp up RF power based on viscosity and speed *)
        rPullerSpeed_Ref := 2.5; (* Nominal run speed m/s *)
        rRF_Power_Ref := (rPullerSpeed_Act * 10.0) + (rResinViscosity * 0.5); 
        
        (* Transition to fault states if parameters go out of bounds *)
        IF rDieTemp_Act > 220.0 OR rDieTemp_Act < 170.0 THEN
            bCureTempAlarm := TRUE;
        ELSE
            bCureTempAlarm := FALSE;
        END_IF;
        
        (* Dynamic puller slip detection *)
        rExpectedTension := rPullerSpeed_Act * 200.0; 
        IF ABS(rLineTension_Exit - rExpectedTension) > rSlipThreshold THEN
            tSlipDetectTimer(IN := TRUE, PT := T#2S);
            IF tSlipDetectTimer.Q THEN
                bTensionSlipAlarm := TRUE;
                iState := 99; (* FAULT STATE *)
            END_IF;
        ELSE
            tSlipDetectTimer(IN := FALSE);
            bTensionSlipAlarm := FALSE;
        END_IF;

        IF NOT bSystemEnable THEN
            iState := 30; (* RAMP DOWN *)
        END_IF;
        
    30: (* RAMP DOWN & COOLING *)
        rPullerSpeed_Ref := 0.5;
        rRF_Power_Ref := 0.0; (* Cut curing power immediately *)
        tStartupDelay(IN := TRUE, PT := T#15S);
        IF tStartupDelay.Q THEN
            tStartupDelay(IN := FALSE);
            rPullerSpeed_Ref := 0.0;
            rCreelTension_Ref := 0.0;
            iState := 0;
        END_IF;
        
    99: (* FAULT HANDLING *)
        rPullerSpeed_Ref := 0.0;
        rRF_Power_Ref := 0.0;
        (* Maintain tension to prevent fiber nest formation *)
        rCreelTension_Ref := 100.0; 
        
        IF NOT bSystemEnable THEN
            (* Operator reset via disable toggle *)
            bTensionSlipAlarm := FALSE;
            bCureTempAlarm := FALSE;
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

filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
