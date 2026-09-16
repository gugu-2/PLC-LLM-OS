import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: High-Temperature Molten Salt Thermal Energy Storage Pump Station**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 565°C nitrate salt freeze-protection trace heating cascade, vertical cantilever pump thermal gradient startup ramp, and cold-tank/hot-tank differential expansion monitoring). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_MoltenSalt_PumpStation\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: High-Temperature Molten Salt Thermal Energy Storage Pump Station

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_MoltenSalt_PumpStation
VAR_INPUT
    (* Required: at least 4-8 physical inputs with types and comments *)
    bEnable                 : BOOL;     (* System master enable signal *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal (E-Stop) *)
    rSaltTempHotTank        : REAL;     (* Temperature of salt in hot tank [deg C] *)
    rSaltTempColdTank       : REAL;     (* Temperature of salt in cold tank [deg C] *)
    rPumpCasingTemp         : REAL;     (* Vertical cantilever pump casing temp [deg C] *)
    rTraceHeaterTemp        : REAL;     (* Heat trace line temperature [deg C] *)
    rVibrationP2P           : REAL;     (* Pump vibration peak-to-peak [mm/s] *)
    bShaftLock              : BOOL;     (* True if mechanical lock is disengaged *)
END_VAR
VAR_OUTPUT
    (* Required: at least 3-6 outputs with types and comments *)
    bSystemReady            : BOOL;     (* Pump station is ready for operation *)
    rPumpSpeedCmd           : REAL;     (* VFD speed command [%] *)
    bTraceHeaterEnable      : BOOL;     (* Heat trace power enable *)
    bAlarm                  : BOOL;     (* General fault alarm *)
    iFaultCode              : INT;      (* Diagnostics fault code *)
    bPumpPreheatActive      : BOOL;     (* Pump preheating sequence active *)
END_VAR
VAR
    (* Internal state variables *)
    iState                  : INT := 0;
    tPreheatTimer           : TON;
    tStartupTimer           : TON;
    rFilteredVibration      : REAL;
    rDeltaTempH2C           : REAL;
    bTempOkForStart         : BOOL;
    bVibrationAlarm         : BOOL;
END_VAR

(* === MAIN LOGIC === *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bAlarm := TRUE;
    iFaultCode := 999; (* Critical E-Stop *)
    rPumpSpeedCmd := 0.0;
    bTraceHeaterEnable := FALSE;
    bPumpPreheatActive := FALSE;
    iState := 0;
    RETURN;
END_IF;

(* Filter vibration noise (low pass EMA) *)
rFilteredVibration := (0.9 * rFilteredVibration) + (0.1 * rVibrationP2P);

(* Compute thermal gradients *)
rDeltaTempH2C := rSaltTempHotTank - rSaltTempColdTank;
bTempOkForStart := (rPumpCasingTemp > 290.0) AND (rTraceHeaterTemp > 300.0);

(* Vibration Safety Interlock *)
IF rFilteredVibration > 15.0 THEN
    bVibrationAlarm := TRUE;
    bAlarm := TRUE;
    iFaultCode := 101; (* High Vibration *)
    rPumpSpeedCmd := 0.0;
    iState := 99; (* Fault state *)
END_IF;

(* State Machine *)
CASE iState OF
    0: (* IDLE & FREEZE PROTECTION *)
        bSystemReady := FALSE;
        rPumpSpeedCmd := 0.0;
        bPumpPreheatActive := FALSE;
        
        (* Trace Heating Freeze Protection Loop *)
        IF rTraceHeaterTemp < 280.0 THEN
            bTraceHeaterEnable := TRUE;
        ELSIF rTraceHeaterTemp > 310.0 THEN
            bTraceHeaterEnable := FALSE;
        END_IF;
        
        IF bEnable AND bShaftLock AND NOT bVibrationAlarm THEN
            IF bTempOkForStart THEN
                iState := 20; (* Ready to ramp *)
            ELSE
                iState := 10; (* Entering Preheat *)
            END_IF;
        END_IF;

    10: (* PREHEAT SEQUENCE *)
        bPumpPreheatActive := TRUE;
        bTraceHeaterEnable := TRUE; (* Force trace heating *)
        tPreheatTimer(IN := TRUE, PT := T#30M);
        
        IF bTempOkForStart THEN
            tPreheatTimer(IN := FALSE);
            iState := 20;
        ELSIF tPreheatTimer.Q THEN
            (* Failed to preheat within 30 min *)
            bAlarm := TRUE;
            iFaultCode := 201; (* Preheat Timeout *)
            iState := 99;
        END_IF;
        IF NOT bEnable THEN iState := 0; END_IF;

    20: (* READY / PRE-START *)
        bSystemReady := TRUE;
        bPumpPreheatActive := FALSE;
        IF bEnable THEN
            tStartupTimer(IN := TRUE, PT := T#10S);
            rPumpSpeedCmd := 5.0; (* 5% minimal bearing lubrication speed *)
            IF tStartupTimer.Q THEN
                tStartupTimer(IN := FALSE);
                iState := 30;
            END_IF;
        ELSE
            iState := 0;
        END_IF;

    30: (* RAMPING TO NOMINAL *)
        bSystemReady := TRUE;
        IF rPumpSpeedCmd < 100.0 THEN
            rPumpSpeedCmd := rPumpSpeedCmd + 0.1; (* Ramp up *)
        END_IF;
        
        IF NOT bEnable THEN
            iState := 0; (* Direct cutoff *)
        END_IF;

    99: (* FAULT HANDLING *)
        bSystemReady := FALSE;
        rPumpSpeedCmd := 0.0;
        bTraceHeaterEnable := TRUE; (* Keep molten *)
        (* Wait for operator reset which could be a specific toggle of bEnable *)
        IF NOT bEnable AND NOT bEmergencyStop THEN
            bAlarm := FALSE;
            bVibrationAlarm := FALSE;
            iFaultCode := 0;
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

filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
