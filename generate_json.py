import json, uuid
import os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Commercial Water Park Wave Pool Pneumatic Caisson and Filtration Cycle**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_WavePool_Control\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Commercial Water Park Wave Pool Pneumatic Caisson and Filtration Cycle

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_WavePool_Pneumatic_Caisson_Filtration
VAR_INPUT
    (* Safety and Enable *)
    bSystemEnable           : BOOL;     (* Main system enable signal *)
    bEmergencyStopOk        : BOOL;     (* Safety loop OK, normally high *)
    bLifeguardOverride      : BOOL;     (* Manual emergency kill from lifeguard tower *)
    bMaintenanceMode        : BOOL;     (* Maintenance mode active *)
    
    (* Process Variables - Analog Inputs *)
    rCaissonAirPressure     : REAL;     (* Current air pressure in pneumatic caissons (bar) *)
    rPoolWaterLevel         : REAL;     (* Water level in main pool (meters) *)
    rFilterDeltaPressure    : REAL;     (* Pressure drop across main sand filters (bar) *)
    rWaterTurbidity         : REAL;     (* Water clarity measurement (NTU) *)
    
    (* Configuration Parameters *)
    iWavePattern            : INT;      (* Selected wave pattern: 1=Rolling, 2=Diamond, 3=Tsunami *)
END_VAR

VAR_OUTPUT
    (* Actuator Controls *)
    rBlowerVFDCommand       : REAL;     (* VFD speed command to main air blowers (0-100%) *)
    bCaissonValves          : ARRAY[1..8] OF BOOL; (* High-speed exhaust valves for caissons *)
    bFiltrationPumpEnable   : BOOL;     (* Enable signal for main filtration pumps *)
    bBackwashValve          : BOOL;     (* Actuate sand filter backwash sequence *)
    
    (* Status and Alarms *)
    bSystemReady            : BOOL;     (* System is primed and ready to generate waves *)
    bAlarmActive            : BOOL;     (* General fault alarm *)
    iErrorCode              : INT;      (* Diagnostics code for SCADA *)
END_VAR

VAR
    (* Internal State and Timers *)
    iState                  : INT := 0; (* Main state machine variable *)
    tStartupDelay           : TON;      (* Delay timer for blower startup sequence *)
    tWaveCycleTimer         : TON;      (* Timer for coordinating valve opening *)
    tBackwashTimer          : TON;      (* Duration of filter backwash *)
    
    (* Signal Filtering *)
    rFilteredLevel          : REAL;
    rFilteredPressure       : REAL;
    
    (* Loop Counters and Flags *)
    i                       : INT;
    bWaveInProgress         : BOOL;
    
    (* Constants *)
    rMaxSafePressure        : REAL := 2.5; (* Maximum caisson pressure (bar) *)
    rMinSafeWaterLevel      : REAL := 1.2; (* Minimum water level to run waves (meters) *)
    rBackwashTriggerDP      : REAL := 1.8; (* DP at which to trigger backwash (bar) *)
END_VAR

(* === MAIN LOGIC === *)

(* 1. Critical Safety Interlocks *)
IF NOT bEmergencyStopOk OR bLifeguardOverride THEN
    (* Immediate safe shutdown *)
    bSystemReady := FALSE;
    bAlarmActive := TRUE;
    rBlowerVFDCommand := 0.0;
    bFiltrationPumpEnable := FALSE;
    bBackwashValve := FALSE;
    FOR i := 1 TO 8 DO
        bCaissonValves[i] := FALSE; (* Close all high-speed valves to prevent accidental waves *)
    END_FOR;
    iState := 999; (* Enter fault state *)
    iErrorCode := 1001; (* E-STOP OR OVERRIDE *)
    RETURN;
END_IF;

(* 2. Input Signal Conditioning (First Order Low Pass Filter for noise) *)
rFilteredLevel := (rFilteredLevel * 0.8) + (rPoolWaterLevel * 0.2);
rFilteredPressure := (rFilteredPressure * 0.9) + (rCaissonAirPressure * 0.1);

(* 3. Operational State Machine *)
CASE iState OF
    0: (* IDLE & INITIALIZATION *)
        bSystemReady := FALSE;
        rBlowerVFDCommand := 0.0;
        bFiltrationPumpEnable := TRUE; (* Keep filtration running in idle *)
        
        FOR i := 1 TO 8 DO
            bCaissonValves[i] := FALSE;
        END_FOR;

        IF bSystemEnable AND NOT bMaintenanceMode THEN
            IF rFilteredLevel >= rMinSafeWaterLevel THEN
                iState := 10;
                iErrorCode := 0;
            ELSE
                bAlarmActive := TRUE;
                iErrorCode := 2001; (* LOW WATER LEVEL *)
            END_IF;
        END_IF;

    10: (* PRIMING CAISSONS *)
        bAlarmActive := FALSE;
        rBlowerVFDCommand := 60.0; (* Ramp blowers to 60% *)
        
        tStartupDelay(IN := TRUE, PT := T#15S);
        IF tStartupDelay.Q THEN
            IF rFilteredPressure > 1.0 AND rFilteredPressure < rMaxSafePressure THEN
                tStartupDelay(IN := FALSE);
                iState := 20; (* Ready *)
            ELSE
                tStartupDelay(IN := FALSE);
                bAlarmActive := TRUE;
                iErrorCode := 2002; (* PRESSURE FAULT DURING PRIME *)
                iState := 0;
            END_IF;
        END_IF;

    20: (* READY TO GENERATE WAVES *)
        bSystemReady := TRUE;
        rBlowerVFDCommand := 80.0; (* Maintain ready pressure *)
        
        (* Continuous Filtration Monitoring *)
        IF rFilterDeltaPressure >= rBackwashTriggerDP OR rWaterTurbidity > 5.0 THEN
            iState := 50; (* Jump to backwash *)
        END_IF;

        (* Start wave cycle based on pattern *)
        IF iWavePattern > 0 THEN
            bWaveInProgress := TRUE;
            iState := 30;
        END_IF;

    30: (* WAVE GENERATION CYCLE *)
        tWaveCycleTimer(IN := TRUE, PT := T#3S);
        
        IF iWavePattern = 1 THEN
            (* Rolling wave pattern *)
            bCaissonValves[1] := TRUE;
            bCaissonValves[2] := TRUE;
        ELSIF iWavePattern = 2 THEN
            (* Diamond wave pattern *)
            bCaissonValves[3] := TRUE;
            bCaissonValves[6] := TRUE;
        ELSE
            (* Tsunami pattern - max power *)
            FOR i := 1 TO 8 DO
                bCaissonValves[i] := TRUE;
            END_FOR;
        END_IF;
        
        IF tWaveCycleTimer.Q THEN
            tWaveCycleTimer(IN := FALSE);
            FOR i := 1 TO 8 DO
                bCaissonValves[i] := FALSE;
            END_FOR;
            bWaveInProgress := FALSE;
            iState := 20; (* Return to ready *)
        END_IF;

    50: (* AUTOMATED BACKWASH CYCLE *)
        bSystemReady := FALSE;
        bFiltrationPumpEnable := FALSE; (* Stop main flow momentarily *)
        bBackwashValve := TRUE; (* Actuate backwash sequence *)
        
        tBackwashTimer(IN := TRUE, PT := T#120S); (* 2-minute backwash *)
        
        IF tBackwashTimer.Q THEN
            tBackwashTimer(IN := FALSE);
            bBackwashValve := FALSE;
            bFiltrationPumpEnable := TRUE;
            iState := 0; (* Return to idle and check everything *)
        END_IF;

    999: (* FAULT LOCKOUT *)
        IF NOT bAlarmActive AND bSystemEnable = FALSE THEN
            iState := 0; (* Reset required to clear fault state *)
        END_IF;

END_CASE;

(* 4. Final Protection Limits on Outputs *)
IF rBlowerVFDCommand > 100.0 THEN
    rBlowerVFDCommand := 100.0;
END_IF;

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
