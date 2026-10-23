import os
import json
import uuid

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Industrial Scale Liquid Air Energy Storage (LAES) Cryo-Turbine**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., -196°C liquid air isentropic expansion, cold box thermal inventory rock-bed cycling, and synchronous generator inertia frequency response). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_LAES_CryoTurbine\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Scale Liquid Air Energy Storage (LAES) Cryo-Turbine

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_LAES_CryoTurbine
VAR_INPUT
    bEnable                 : BOOL;     (* Main enable signal for turbine start sequence *)
    bEmergencyStop          : BOOL;     (* Safety loop status, TRUE = OK to run *)
    rInletTempCryo          : REAL;     (* Liquid air inlet temperature before expansion in DegC (approx -196) *)
    rInletPressCryo         : REAL;     (* Inlet pressure from cryogenic pumps in bar *)
    rGridFrequency          : REAL;     (* Synchronous generator grid frequency in Hz *)
    rRockBedThermalInv      : REAL;     (* Thermal inventory level of the cold box rock-bed in % *)
    bSynchronizeCommand     : BOOL;     (* Command to synchronize generator with grid *)
    rTargetLoadMW           : REAL;     (* Target generation load in MW *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* System ready for expansion phase *)
    bGridSynchronized       : BOOL;     (* Generator successfully synchronized to grid *)
    rValvePosGovernor       : REAL;     (* Commanded position for the main governor valve (0-100%) *)
    rActivePowerMW          : REAL;     (* Calculated active power output in MW *)
    rExhaustTemp            : REAL;     (* Exhaust air temperature after expansion in DegC *)
    bThermalAlarm           : BOOL;     (* Alarm indicating thermal shock risk or depletion *)
    bTripActivated          : BOOL;     (* Critical trip has been activated *)
END_VAR
VAR
    iState                  : INT := 0; (* Internal state machine *)
    tPrecoolTimer           : TON;      (* Timer for pre-cooling sequence *)
    tSyncTimer              : TON;      (* Timer for synchronization phase *)
    rTurbineSpeedRPM        : REAL := 0.0;
    rIsentropicEff          : REAL := 0.85; (* Assumed isentropic efficiency *)
    rGasConstantAir         : REAL := 287.058;
    rGamma                  : REAL := 1.4;
    rPressureRatio          : REAL;
END_VAR

(* === SAFETY AND INTERLOCKS === *)
IF NOT bEmergencyStop THEN
    bSystemReady      := FALSE;
    bGridSynchronized := FALSE;
    bTripActivated    := TRUE;
    rValvePosGovernor := 0.0;
    iState            := 999; (* Trip state *)
    RETURN;
END_IF;

IF rInletTempCryo > -170.0 AND iState > 0 AND iState < 999 THEN
    (* Inlet temperature too high, risk of losing liquid phase prematurely or thermal shock *)
    bThermalAlarm := TRUE;
    IF rInletTempCryo > -150.0 THEN
        bTripActivated := TRUE;
        rValvePosGovernor := 0.0;
        iState := 999;
    END_IF;
ELSE
    bThermalAlarm := FALSE;
END_IF;

(* === MAIN STATE MACHINE === *)
CASE iState OF
    0: (* IDLE / READY TO START *)
        bSystemReady := TRUE;
        bTripActivated := FALSE;
        rValvePosGovernor := 0.0;
        rActivePowerMW := 0.0;
        
        IF bEnable AND bSystemReady THEN
            iState := 10; (* Transition to Pre-cooling *)
        END_IF;

    10: (* PRE-COOLING CRYO-TURBINE CASING *)
        bSystemReady := FALSE;
        (* Open governor valve slightly to allow cryogenic bleed for casing cool-down *)
        rValvePosGovernor := 5.0; 
        
        tPrecoolTimer(IN := TRUE, PT := T#5M); (* 5 minutes precool *)
        IF tPrecoolTimer.Q THEN
            tPrecoolTimer(IN := FALSE);
            iState := 20; (* Ramp up to nominal speed *)
        END_IF;

    20: (* SPEED RAMP-UP TO SYNCHRONOUS SPEED *)
        (* Governor PID control would go here, simulated by fixed ramp *)
        IF rTurbineSpeedRPM < 3000.0 THEN
            rValvePosGovernor := rValvePosGovernor + 0.1;
            rTurbineSpeedRPM := rTurbineSpeedRPM + 15.0;
        ELSE
            iState := 30; (* Waiting for sync command *)
        END_IF;

    30: (* WAITING FOR SYNCHRONIZATION *)
        IF bSynchronizeCommand THEN
            tSyncTimer(IN := TRUE, PT := T#10S);
            (* Simulate synch check relay *)
            IF tSyncTimer.Q AND ABS(rGridFrequency - 50.0) < 0.1 THEN
                bGridSynchronized := TRUE;
                tSyncTimer(IN := FALSE);
                iState := 40; (* Loaded operation *)
            END_IF;
        ELSE
            tSyncTimer(IN := FALSE);
        END_IF;

    40: (* LOADED OPERATION & FREQUENCY RESPONSE *)
        (* Thermodynamic calculation for exhaust temp (T2 = T1 * (P2/P1)^((g-1)/g)) *)
        IF rInletPressCryo > 1.0 THEN
            rPressureRatio := 1.0 / rInletPressCryo; (* Assuming exhaust to 1 bar *)
            rExhaustTemp := (rInletTempCryo + 273.15) * EXPT(rPressureRatio, (rGamma - 1.0)/rGamma);
            rExhaustTemp := rExhaustTemp - 273.15; (* Convert back to Celsius *)
        ELSE
            rExhaustTemp := rInletTempCryo;
        END_IF;

        (* Load control based on frequency droop and target MW *)
        IF rGridFrequency < 49.5 THEN
            (* Primary frequency response: open valve to provide inertia/power *)
            rValvePosGovernor := LIMIT(0.0, rValvePosGovernor + 5.0, 100.0);
        ELSIF rGridFrequency > 50.5 THEN
            rValvePosGovernor := LIMIT(0.0, rValvePosGovernor - 5.0, 100.0);
        ELSE
            (* Track target load *)
            rValvePosGovernor := (rTargetLoadMW / 50.0) * 100.0; (* Assuming 50MW base *)
            rValvePosGovernor := LIMIT(0.0, rValvePosGovernor, 100.0);
        END_IF;

        rActivePowerMW := (rValvePosGovernor / 100.0) * 50.0;

        IF NOT bEnable THEN
            bGridSynchronized := FALSE;
            rValvePosGovernor := 0.0;
            iState := 50; (* Spindown *)
        END_IF;

    50: (* SPINDOWN *)
        rTurbineSpeedRPM := rTurbineSpeedRPM - 20.0;
        IF rTurbineSpeedRPM <= 0.0 THEN
            rTurbineSpeedRPM := 0.0;
            iState := 0;
        END_IF;

    999: (* TRIP STATE *)
        rValvePosGovernor := 0.0;
        rActivePowerMW := 0.0;
        bGridSynchronized := FALSE;
        IF bEmergencyStop AND NOT bEnable THEN
            (* Reset condition *)
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
