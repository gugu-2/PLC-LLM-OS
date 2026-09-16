import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: High-Speed Pharmaceutical Glass Vial Lyophilization Vacuum Profiling**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Pharma_Lyophilization\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: High-Speed Pharmaceutical Glass Vial Lyophilization Vacuum Profiling

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_Pharma_Lyo_Vacuum_Profile
VAR_INPUT
    bEnable                 : BOOL;     (* Main sequence enable signal *)
    bEmergencyStop          : BOOL;     (* E-Stop safety relay interlock (TRUE = OK) *)
    bChamberDoorClosed      : BOOL;     (* Proximity sensor confirming door is sealed *)
    rChamberPressure        : REAL;     (* Current chamber pressure (mBar) from Pirani gauge *)
    rCondenserTemp          : REAL;     (* Condenser surface temperature (deg C) *)
    rShelfTemp              : REAL;     (* Product shelf temperature (deg C) *)
    rTargetVacuum           : REAL;     (* Setpoint for primary drying vacuum (mBar) *)
    rMaxVacuumDeviation     : REAL;     (* Max allowable deviation from setpoint (mBar) *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* Indicates system is ready to begin evacuation *)
    rVacuumValveCmd         : REAL;     (* Output to proportional vacuum control valve (0-100%) *)
    bVacuumPumpRun          : BOOL;     (* Command to start main vacuum pump *)
    bBleedValveOpen         : BOOL;     (* Command to open sterile N2 bleed valve *)
    bAlarmVacuumLoss        : BOOL;     (* Alarm: Loss of vacuum or failure to reach setpoint *)
    bAlarmCondenserWarm     : BOOL;     (* Alarm: Condenser temp too high for safe evacuation *)
    iCurrentPhase           : INT;      (* Current sequence phase mapping *)
END_VAR
VAR
    iState                  : INT := 0; (* Internal state machine step *)
    rFilteredPressure       : REAL;     (* Low-pass filtered pressure reading *)
    rPressureError          : REAL;     (* Error between setpoint and actual pressure *)
    rIntegral               : REAL := 0.0; (* PID Integral term *)
    rDerivative             : REAL;     (* PID Derivative term *)
    rLastPressure           : REAL := 0.0; (* Last pressure for derivative calculation *)
    tStateTimer             : TON;      (* Timer for state transitions and timeouts *)
    tEvacuationTimer        : TON;      (* Maximum allowed time for initial pump down *)
    tPidUpdateTimer         : TON;      (* Timer for discrete PID execution *)
    
    (* Filter constants *)
    rAlpha                  : REAL := 0.2; (* Filter coefficient (0-1) *)
    
    (* PID tuning constants for vacuum control *)
    rKp                     : REAL := 2.5; 
    rKi                     : REAL := 0.8;
    rKd                     : REAL := 0.1;
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety Interlocks and Global Error Handling *)
IF NOT bEmergencyStop THEN
    iState := 999; (* Transition to Safe/Fault State *)
    bSystemReady := FALSE;
    bVacuumPumpRun := FALSE;
    rVacuumValveCmd := 0.0;
    bBleedValveOpen := TRUE; (* Flood chamber with sterile gas to prevent back-streaming *)
    iCurrentPhase := iState;
    RETURN;
END_IF;

(* 2. Condenser Protection *)
IF rCondenserTemp > -45.0 THEN
    bAlarmCondenserWarm := TRUE;
    IF iState > 10 AND iState < 900 THEN
        iState := 999; (* Abort vacuum if condenser loses cooling capacity *)
    END_IF;
ELSE
    bAlarmCondenserWarm := FALSE;
END_IF;

(* 3. Sensor Noise Filtering (Low-Pass Filter on Pirani Gauge) *)
rFilteredPressure := (rAlpha * rChamberPressure) + ((1.0 - rAlpha) * rFilteredPressure);

(* 4. Main State Machine *)
CASE iState OF
    0: (* IDLE & CHECKS *)
        bVacuumPumpRun := FALSE;
        rVacuumValveCmd := 0.0;
        bBleedValveOpen := FALSE;
        bAlarmVacuumLoss := FALSE;
        
        IF bChamberDoorClosed AND NOT bAlarmCondenserWarm THEN
            bSystemReady := TRUE;
            IF bEnable THEN
                bSystemReady := FALSE;
                iState := 10; (* Transition to Start Pump Down *)
            END_IF;
        ELSE
            bSystemReady := FALSE;
        END_IF;

    10: (* ROUGHING PUMP DOWN PHASE *)
        bVacuumPumpRun := TRUE;
        rVacuumValveCmd := 100.0; (* Full open to pump *)
        bBleedValveOpen := FALSE;
        
        tEvacuationTimer(IN := TRUE, PT := T#10M); (* 10 minutes max to reach rough vacuum *)
        
        IF rFilteredPressure <= (rTargetVacuum * 1.5) THEN
            tEvacuationTimer(IN := FALSE);
            iState := 20; (* Transition to Fine Control *)
        ELSIF tEvacuationTimer.Q THEN
            tEvacuationTimer(IN := FALSE);
            bAlarmVacuumLoss := TRUE;
            iState := 999; (* Timeout fault *)
        END_IF;

    20: (* PID VACUUM PROFILING PHASE (PRIMARY DRYING) *)
        tPidUpdateTimer(IN := TRUE, PT := T#100MS);
        
        IF tPidUpdateTimer.Q THEN
            tPidUpdateTimer(IN := FALSE);
            
            (* Calculate Error *)
            rPressureError := rFilteredPressure - rTargetVacuum;
            
            (* Integral Accumulation with Anti-Windup *)
            IF (rVacuumValveCmd < 100.0) AND (rVacuumValveCmd > 0.0) THEN
                rIntegral := rIntegral + (rPressureError * rKi);
            END_IF;
            
            (* Derivative Calculation *)
            rDerivative := (rFilteredPressure - rLastPressure) * rKd;
            rLastPressure := rFilteredPressure;
            
            (* Compute Control Output *)
            rVacuumValveCmd := (rPressureError * rKp) + rIntegral + rDerivative;
            
            (* Clamp Output 0-100% *)
            IF rVacuumValveCmd > 100.0 THEN
                rVacuumValveCmd := 100.0;
            ELSIF rVacuumValveCmd < 0.0 THEN
                rVacuumValveCmd := 0.0;
            END_IF;
        END_IF;
        
        (* Monitor for deviation faults *)
        IF ABS(rFilteredPressure - rTargetVacuum) > rMaxVacuumDeviation THEN
            tStateTimer(IN := TRUE, PT := T#30S);
            IF tStateTimer.Q THEN
                bAlarmVacuumLoss := TRUE;
                iState := 999;
            END_IF;
        ELSE
            tStateTimer(IN := FALSE);
        END_IF;
        
        (* Completion Condition *)
        IF NOT bEnable THEN
            tStateTimer(IN := FALSE);
            tPidUpdateTimer(IN := FALSE);
            iState := 30;
        END_IF;

    30: (* NORMAL SHUTDOWN / AERATION *)
        bVacuumPumpRun := FALSE;
        rVacuumValveCmd := 0.0;
        bBleedValveOpen := TRUE; (* Bring chamber back to atmospheric pressure *)
        
        IF rFilteredPressure >= 950.0 THEN (* Approx atmospheric *)
            bBleedValveOpen := FALSE;
            iState := 0;
        END_IF;

    999: (* FAULT HANDLING *)
        bVacuumPumpRun := FALSE;
        rVacuumValveCmd := 0.0;
        
        (* Do not bleed automatically on all faults, wait for operator reset *)
        IF NOT bEnable AND NOT bEmergencyStop THEN
            (* Operator cleared enable and E-Stop is OK *)
            bAlarmVacuumLoss := FALSE;
            iState := 0;
        END_IF;

END_CASE;

iCurrentPhase := iState;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print("done")
