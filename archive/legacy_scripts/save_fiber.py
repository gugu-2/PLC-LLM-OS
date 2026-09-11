import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Automated Optical Fiber Draw Tower Preform Feeding**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 2000°C graphite furnace temperature profiling, sub-micron diameter feedback via laser micrometer, dynamic draw tension capstan control, and helium cooling tube cascaded pressure). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_OpticalFiberDraw\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Automated Optical Fiber Draw Tower Preform Feeding

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_OptFiberDrawTower_PreformFeed
VAR_INPUT
    (* High-precision physical inputs from sensors *)
    bSystemEnable       : BOOL;     (* Main draw tower sequence enable signal *)
    bEStop_OK           : BOOL;     (* Safety relay loop closed and OK *)
    rFurnaceTemp_C      : REAL;     (* 2000C graphite furnace pyrometer feedback *)
    rFiberDiameter_um   : REAL;     (* Sub-micron diameter feedback via laser micrometer *)
    rTensionLoad_N      : REAL;     (* Dynamic draw tension feedback from capstan load cell *)
    rPreformPosition_mm : LREAL;    (* Absolute linear encoder feedback for preform Z-axis position *)
    bHeliumFlowOK       : BOOL;     (* Helium cooling tube cascaded pressure OK status *)
    rLineSpeed_mps      : REAL;     (* Current line speed in meters per second *)
END_VAR
VAR_OUTPUT
    (* Actuator setpoints and status *)
    bTowerReady         : BOOL;     (* Draw tower pre-conditions satisfied *)
    rPreformFeedSpd_mms : LREAL;    (* Feed rate setpoint for Z-axis servo drive (mm/s) *)
    rCapstanSpeed_mps   : REAL;     (* Capstan take-up speed setpoint (m/s) *)
    bHeaterPowerEnable  : BOOL;     (* Enable signal for furnace induction heater power supply *)
    rHeaterPower_Pct    : REAL;     (* 0-100% power command for furnace temperature control *)
    bTensionAlarm       : BOOL;     (* Out-of-bounds tension alarm *)
    bDiameterAlarm      : BOOL;     (* Out-of-bounds diameter control alarm *)
    iDrawState          : INT;      (* Current state of the draw machine sequence *)
END_VAR
VAR
    (* Internal PID and state variables *)
    iState              : INT := 0;
    tSoakTimer          : TON;
    tTensionFilter      : TON;
    
    (* Diameter PID Controller Variables *)
    rDiaError           : REAL;
    rDiaIntegral        : REAL;
    rDiaDerivative      : REAL;
    rDiaPrevError       : REAL;
    rKp_Dia             : REAL := 1.25;
    rKi_Dia             : REAL := 0.05;
    rKd_Dia             : REAL := 0.01;
    
    (* Temperature Control Variables *)
    rTempSetPoint       : REAL := 2050.0;
    rTempError          : REAL;
    
    (* Process Constants *)
    rTargetDiameter     : REAL := 125.0; (* 125 microns standard fiber *)
    rMaxTension         : REAL := 1.5;   (* 1.5 N max draw tension *)
    rMinTension         : REAL := 0.3;   (* 0.3 N min draw tension *)
END_VAR

(* === MAIN LOGIC === *)
(* Emergency and Safety Interlocks *)
IF NOT bEStop_OK THEN
    bTowerReady         := FALSE;
    bHeaterPowerEnable  := FALSE;
    rPreformFeedSpd_mms := 0.0;
    rCapstanSpeed_mps   := 0.0;
    rHeaterPower_Pct    := 0.0;
    bTensionAlarm       := TRUE;
    bDiameterAlarm      := TRUE;
    iState              := 99; (* Fault state *)
    RETURN;
END_IF;

(* Clear alarms if safety is OK and not in fault *)
IF iState <> 99 THEN
    bTensionAlarm       := FALSE;
    bDiameterAlarm      := FALSE;
END_IF;

(* Draw Tower State Machine *)
CASE iState OF
    0: (* IDLE - Wait for System Enable and cooling ready *)
        bTowerReady := FALSE;
        rPreformFeedSpd_mms := 0.0;
        rCapstanSpeed_mps := 0.0;
        rHeaterPower_Pct := 0.0;
        bHeaterPowerEnable := FALSE;
        
        IF bSystemEnable AND bHeliumFlowOK THEN
            iState := 10;
        END_IF;

    10: (* FURNACE PREHEAT - Ramp temperature to setpoint *)
        bHeaterPowerEnable := TRUE;
        rTempError := rTempSetPoint - rFurnaceTemp_C;
        
        (* Simple P-control for furnace power as demonstration *)
        rHeaterPower_Pct := rTempError * 0.5 + 50.0;
        
        IF rHeaterPower_Pct > 100.0 THEN
            rHeaterPower_Pct := 100.0;
        ELSIF rHeaterPower_Pct < 0.0 THEN
            rHeaterPower_Pct := 0.0;
        END_IF;
        
        IF rFurnaceTemp_C >= (rTempSetPoint - 5.0) THEN
            iState := 20;
        END_IF;

    20: (* THERMAL SOAK - Stabilize preform neck-down region *)
        tSoakTimer(IN := TRUE, PT := T#300S); (* 5 minute soak *)
        
        IF tSoakTimer.Q THEN
            tSoakTimer(IN := FALSE);
            iState := 30;
        END_IF;

    30: (* DRAW INITIATION - Start preform feed and capstan slow pull *)
        bTowerReady := TRUE;
        rPreformFeedSpd_mms := 0.01; (* Very slow initial feed *)
        rCapstanSpeed_mps := 0.5;    (* Slow initial draw speed *)
        
        IF rTensionLoad_N > 0.5 THEN
            iState := 40;
        END_IF;

    40: (* CLOSED LOOP DRAW - Active diameter and tension control *)
        (* Diameter PID loop to adjust capstan speed *)
        rDiaError := rTargetDiameter - rFiberDiameter_um;
        rDiaIntegral := rDiaIntegral + rDiaError;
        rDiaDerivative := rDiaError - rDiaPrevError;
        
        rCapstanSpeed_mps := rCapstanSpeed_mps + (rKp_Dia * rDiaError) + (rKi_Dia * rDiaIntegral) + (rKd_Dia * rDiaDerivative);
        rDiaPrevError := rDiaError;
        
        (* Tension limits monitoring *)
        IF rTensionLoad_N > rMaxTension OR rTensionLoad_N < rMinTension THEN
            tTensionFilter(IN := TRUE, PT := T#2S);
            IF tTensionFilter.Q THEN
                bTensionAlarm := TRUE;
                iState := 99; (* Abort to fault state *)
            END_IF;
        ELSE
            tTensionFilter(IN := FALSE);
        END_IF;
        
        (* Diameter fault check *)
        IF ABS(rDiaError) > 5.0 THEN
            bDiameterAlarm := TRUE;
        END_IF;
        
        (* Check if disabled *)
        IF NOT bSystemEnable THEN
            iState := 0;
        END_IF;
        
    99: (* FAULT STATE *)
        bTowerReady := FALSE;
        rPreformFeedSpd_mms := 0.0;
        rCapstanSpeed_mps := 0.0;
        bHeaterPowerEnable := FALSE;
        rHeaterPower_Pct := 0.0;
        
        IF NOT bSystemEnable THEN
            (* Require enable signal cycle to reset fault *)
            iState := 0;
        END_IF;

END_CASE;

(* Expose internal state to output *)
iDrawState := iState;

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
