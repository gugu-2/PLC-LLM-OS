import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Commercial Ship Engine Room Heavy Fuel Oil (HFO) Purifier Desludging Cascade**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Marine_HFOPurifier\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Commercial Ship Engine Room Heavy Fuel Oil (HFO) Purifier Desludging Cascade

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_Marine_HFOPurifier
VAR_INPUT
    bSystemEnable         : BOOL;     (* Main HFO purifier system enable from ship power management *)
    bEmergencyStop        : BOOL;     (* Safety relay OK signal from engine room E-Stop loop *)
    rHFO_Temp             : REAL;     (* Heavy Fuel Oil temperature at purifier inlet [deg C] *)
    rBowlSpeed            : REAL;     (* Purifier bowl rotational speed [RPM] *)
    bSludgeTankHigh       : BOOL;     (* Sludge holding tank high level switch *)
    rWaterTransducer      : REAL;     (* Water content in oil transducer [ppm] *)
    bSealWaterPressureOK  : BOOL;     (* Bowl closing water seal pressure sufficient *)
END_VAR
VAR_OUTPUT
    bSystemReady          : BOOL;     (* Purifier ready for continuous separation *)
    bDesludgeActive       : BOOL;     (* Desludging (shooting) cycle currently active *)
    rFeedPumpCmd          : REAL;     (* VFD command for HFO feed pump [0-100%] *)
    bDischargeValve       : BOOL;     (* Sludge discharge valve control signal *)
    bAlarm                : BOOL;     (* Fault alarm output (temperature, speed, or level) *)
END_VAR
VAR
    iDesludgeState        : INT := 0;
    tShootTimer           : TON;
    tDwellTimer           : TON;
    rTempSetPoint         : REAL := 98.0; (* Optimal HFO separation temperature [deg C] *)
    rFilteredTemp         : REAL := 0.0;
    rFilteredTempOld      : REAL := 0.0;
    rAlpha                : REAL := 0.1;  (* EWMA filter coefficient for sensor noise *)
    iCyclesSinceClean     : DINT := 0;
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety & Interlocks *)
IF NOT bEmergencyStop OR bSludgeTankHigh THEN
    bSystemReady := FALSE;
    bDesludgeActive := FALSE;
    rFeedPumpCmd := 0.0;
    bDischargeValve := FALSE;
    bAlarm := TRUE;
    iDesludgeState := 0;
    RETURN;
END_IF;

(* 2. Sensor Noise Filtering (EWMA) *)
rFilteredTemp := (rAlpha * rHFO_Temp) + ((1.0 - rAlpha) * rFilteredTempOld);
rFilteredTempOld := rFilteredTemp;

(* 3. Operational Readiness Check *)
IF bSystemEnable AND (rFilteredTemp >= rTempSetPoint - 2.0) AND (rBowlSpeed > 7500.0) AND bSealWaterPressureOK THEN
    bSystemReady := TRUE;
    bAlarm := FALSE;
ELSE
    bSystemReady := FALSE;
    rFeedPumpCmd := 0.0;
END_IF;

(* 4. Desludge State Machine (Cascade) *)
CASE iDesludgeState OF
    0: (* IDLE / SEPARATING *)
        IF bSystemReady THEN
            rFeedPumpCmd := 100.0; (* Full feed rate during normal operation *)
            bDesludgeActive := FALSE;
            bDischargeValve := FALSE;
            
            (* Trigger desludge based on high water content or periodic cycle (simulated by cycles count here) *)
            IF rWaterTransducer > 2000.0 OR iCyclesSinceClean > 100000 THEN
                iDesludgeState := 10;
                iCyclesSinceClean := 0;
            ELSE
                iCyclesSinceClean := iCyclesSinceClean + 1;
            END_IF;
        END_IF;

    10: (* PRE-SHOOT SEQUENCE - SHUT OFF FEED *)
        rFeedPumpCmd := 0.0;
        bDesludgeActive := TRUE;
        tShootTimer(IN := TRUE, PT := T#3S);
        IF tShootTimer.Q THEN
            tShootTimer(IN := FALSE);
            iDesludgeState := 20;
        END_IF;

    20: (* SHOOT - OPEN DISCHARGE VALVE *)
        bDischargeValve := TRUE;
        tDwellTimer(IN := TRUE, PT := T#1S); (* Open for 1 second *)
        IF tDwellTimer.Q THEN
            tDwellTimer(IN := FALSE);
            bDischargeValve := FALSE;
            iDesludgeState := 30;
        END_IF;

    30: (* POST-SHOOT RECOVERY *)
        tShootTimer(IN := TRUE, PT := T#5S); (* Wait for bowl to reseal *)
        IF tShootTimer.Q THEN
            tShootTimer(IN := FALSE);
            IF bSealWaterPressureOK THEN
                iDesludgeState := 0; (* Return to separation *)
            ELSE
                bAlarm := TRUE; (* Failed to reseal *)
                iDesludgeState := 99; (* Fault state *)
            END_IF;
        END_IF;

    99: (* FAULT LOCKOUT *)
        bSystemReady := FALSE;
        rFeedPumpCmd := 0.0;
        bDischargeValve := FALSE;
        IF NOT bSystemEnable THEN
            iDesludgeState := 0; (* Reset fault on enable cycle *)
            bAlarm := FALSE;
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
