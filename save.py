import json, uuid, os

prompt = """<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Automated Hydroelectric Dam Penstock Surge Shaft Level and Francis Turbine Guide Vane Sync**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_HydroDam_TurbineControl\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Automated Hydroelectric Dam Penstock Surge Shaft Level and Francis Turbine Guide Vane Sync

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.
</USER_REQUEST>"""

code = """```iec-st
FUNCTION_BLOCK FB_HydroDam_SurgeShaft_GuideVane_Sync
(* 
   Advanced Control System for Hydroelectric Dam 
   Synchronizing Penstock Surge Shaft Level and Francis Turbine Guide Vanes
   Implements extreme edge-case handling, advanced PID, deadband filtering, and multi-layered safety interlocks.
*)
VAR_INPUT
    bEnableSys                  : BOOL;     (* System global enable command *)
    bEmergencyStop              : BOOL;     (* Safety loop OK - Active High *)
    rSurgeShaftLvl_Sensor1      : REAL;     (* Surge shaft level primary sensor (meters) *)
    rSurgeShaftLvl_Sensor2      : REAL;     (* Surge shaft level redundant sensor (meters) *)
    rGridFrequency              : REAL;     (* Electrical grid frequency (Hz) *)
    rGuideVaneActualPos         : REAL;     (* Actual guide vane opening (0.0 to 100.0 %) *)
    rPenstockPressure           : REAL;     (* Penstock dynamic pressure (Bar) *)
    bGridLoadReject             : BOOL;     (* Grid load rejection event detected *)
END_VAR

VAR_OUTPUT
    bSystemReady                : BOOL;     (* Control system is armed and ready *)
    rGuideVaneCmd               : REAL;     (* Output command to guide vane hydraulic actuator (%) *)
    bSurgeShaftSpillWarning     : BOOL;     (* High level warning for surge shaft *)
    bVibrationTripActive        : BOOL;     (* Emergency trip due to calculated pressure resonance *)
    rCalculatedVanePos          : REAL;     (* Filtered and calculated theoretical vane position *)
    bCritFaultAlarm             : BOOL;     (* Critical fault alarm active *)
END_VAR

VAR
    (* Internal State and Timers *)
    iSyncState                  : INT := 0; 
    tStartupDelay               : TON;
    tEmergencyCloseTimer        : TON;
    tSensorDeviationTimer       : TON;
    
    (* Signal Processing and Filtering *)
    rFilteredLevel              : REAL := 0.0;
    rLvlDeviation               : REAL := 0.0;
    rLevelRateOfChange          : REAL := 0.0;
    rLastLevel                  : REAL := 0.0;
    rAlphaLevelFilter           : REAL := 0.15; (* First-order low pass filter coefficient *)
    
    (* Control Parameters *)
    rKp                         : REAL := 2.5; 
    rKi                         : REAL := 0.5;
    rKd                         : REAL := 0.12;
    rIntegralSum                : REAL := 0.0;
    rLastError                  : REAL := 0.0;
    rError                      : REAL := 0.0;
    
    (* Constants *)
    rMaxSurgeLevel              : REAL := 125.0; (* meters *)
    rMinSurgeLevel              : REAL := 80.0;  (* meters *)
    rNominalFrequency           : REAL := 50.0;  (* Hz *)
    rFrequencyDeadband          : REAL := 0.05;  (* Hz *)
    rMaxGuideVaneRate           : REAL := 5.0;   (* % per cycle max change *)
    rMaxPressureTrip            : REAL := 45.0;  (* Bar *)
END_VAR

(* === MAIN LOGIC === *)

(* Multi-Layered Safety Interlocks *)
IF NOT bEmergencyStop OR rPenstockPressure >= rMaxPressureTrip THEN
    bSystemReady := FALSE;
    bCritFaultAlarm := TRUE;
    
    IF rPenstockPressure >= rMaxPressureTrip THEN
        bVibrationTripActive := TRUE;
    END_IF;
    
    (* Immediate hydraulic close command on safety trip *)
    rGuideVaneCmd := 0.0;
    iSyncState := 99; (* Trip state *)
    RETURN;
END_IF;

(* Sensor Arbitration and Noise Filtering *)
rLvlDeviation := ABS(rSurgeShaftLvl_Sensor1 - rSurgeShaftLvl_Sensor2);
tSensorDeviationTimer(IN := (rLvlDeviation > 2.5), PT := T#2S);

IF tSensorDeviationTimer.Q THEN
    bCritFaultAlarm := TRUE;
    rGuideVaneCmd := 0.0;
    iSyncState := 99;
    RETURN;
END_IF;

(* Average the sensors and apply first order low-pass filter *)
rFilteredLevel := rFilteredLevel + rAlphaLevelFilter * (((rSurgeShaftLvl_Sensor1 + rSurgeShaftLvl_Sensor2) / 2.0) - rFilteredLevel);

(* Calculate Rate of Change for derivative action and surge prediction *)
rLevelRateOfChange := rFilteredLevel - rLastLevel;
rLastLevel := rFilteredLevel;

(* Surge Shaft Level Warnings *)
IF rFilteredLevel > (rMaxSurgeLevel * 0.95) THEN
    bSurgeShaftSpillWarning := TRUE;
ELSE
    bSurgeShaftSpillWarning := FALSE;
END_IF;

(* State Machine for Guide Vane Synchronization *)
CASE iSyncState OF
    0: (* IDLE & SELF-TEST *)
        rGuideVaneCmd := 0.0;
        bSystemReady := FALSE;
        IF bEnableSys AND (rFilteredLevel > rMinSurgeLevel) AND NOT bCritFaultAlarm THEN
            tStartupDelay(IN := TRUE, PT := T#5S);
            IF tStartupDelay.Q THEN
                tStartupDelay(IN := FALSE);
                bSystemReady := TRUE;
                iSyncState := 10; (* Transition to Pre-Sync *)
            END_IF;
        ELSE
            tStartupDelay(IN := FALSE);
        END_IF;
        
    10: (* PRE-SYNC / RAMPING *)
        (* Slowly open guide vanes to minimum synchronous speed position *)
        IF rGuideVaneCmd < 15.0 THEN
            rGuideVaneCmd := rGuideVaneCmd + 0.1; 
        ELSE
            iSyncState := 20; (* Active Load Control *)
        END_IF;
        
        IF bGridLoadReject THEN
            iSyncState := 30;
        END_IF;

    20: (* ACTIVE LOAD / FREQUENCY CONTROL WITH SURGE COMPENSATION *)
        (* Advanced PID Frequency Regulation with Surge Shaft Compensation *)
        
        IF ABS(rGridFrequency - rNominalFrequency) > rFrequencyDeadband THEN
            rError := rNominalFrequency - rGridFrequency;
        ELSE
            rError := 0.0;
        END_IF;
        
        rIntegralSum := rIntegralSum + (rError * rKi);
        
        (* Anti-windup limit for integral *)
        IF rIntegralSum > 50.0 THEN rIntegralSum := 50.0; END_IF;
        IF rIntegralSum < -50.0 THEN rIntegralSum := -50.0; END_IF;
        
        (* Calculate theoretical position based on frequency error *)
        rCalculatedVanePos := (rError * rKp) + rIntegralSum + ((rError - rLastError) * rKd);
        rLastError := rError;
        
        (* Surge Shaft Compensation Layer *)
        (* If level is dropping too fast, throttle back to prevent cavitation and water column separation *)
        IF rLevelRateOfChange < -0.5 THEN
            rCalculatedVanePos := rCalculatedVanePos - 10.0;
        END_IF;
        
        (* Apply maximum rate of change limits to the command *)
        IF (rCalculatedVanePos - rGuideVaneCmd) > rMaxGuideVaneRate THEN
            rGuideVaneCmd := rGuideVaneCmd + rMaxGuideVaneRate;
        ELSIF (rGuideVaneCmd - rCalculatedVanePos) > rMaxGuideVaneRate THEN
            rGuideVaneCmd := rGuideVaneCmd - rMaxGuideVaneRate;
        ELSE
            rGuideVaneCmd := rCalculatedVanePos;
        END_IF;
        
        (* Final absolute limits *)
        IF rGuideVaneCmd > 100.0 THEN rGuideVaneCmd := 100.0; END_IF;
        IF rGuideVaneCmd < 0.0 THEN rGuideVaneCmd := 0.0; END_IF;
        
        IF bGridLoadReject THEN
            iSyncState := 30;
        END_IF;
        IF NOT bEnableSys THEN
            iSyncState := 0;
        END_IF;

    30: (* GRID LOAD REJECTION - CONTROLLED SHUTDOWN *)
        (* Rapidly close guide vanes to prevent runaway, but manage surge shaft level rise (water hammer) *)
        rGuideVaneCmd := rGuideVaneCmd - 2.5; (* Fast close rate *)
        IF rGuideVaneCmd <= 0.0 THEN
            rGuideVaneCmd := 0.0;
            iSyncState := 0;
        END_IF;
        
    99: (* FAULTED / EMERGENCY SHUTDOWN *)
        bSystemReady := FALSE;
        rGuideVaneCmd := 0.0;
        IF bEnableSys = FALSE AND bEmergencyStop = TRUE THEN
            (* Reset logic *)
            bCritFaultAlarm := FALSE;
            bVibrationTripActive := FALSE;
            iSyncState := 0;
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("c:/Users/majip/Downloads/LLM REASEARCH/data/swarm_raw", exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
with open(f"c:/Users/majip/Downloads/LLM REASEARCH/data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
