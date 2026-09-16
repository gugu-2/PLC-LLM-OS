import json, uuid, os
os.makedirs('data/swarm_raw', exist_ok=True)
prompt = """<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Autonomous Deep-Shaft Mine Ventilation and Toxic Gas Extraction Cascade**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Mine_VentilationCascade\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Autonomous Deep-Shaft Mine Ventilation and Toxic Gas Extraction Cascade

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.
</USER_REQUEST>"""

code = """```iec-st
FUNCTION_BLOCK FB_Mine_VentilationCascade

(*========================================================================================
   FUNCTION BLOCK: FB_Mine_VentilationCascade
   DESCRIPTION: Autonomous Deep-Shaft Mine Ventilation and Toxic Gas Extraction Cascade.
   This FB manages the main and auxiliary ventilation fans, toxic gas extraction logic,
   and personnel safety interlocks for deep-shaft mining environments.
   Features:
   - Multi-gas (CO, CH4, NO2) sensor fusion and moving average filtering.
   - Fault-tolerant PID control for variable frequency drives (VFD) controlling main fans.
   - Emergency cascade extraction override on critical gas levels.
   - Personnel tracking interlock for blast zones and extraction chambers.
========================================================================================*)

VAR_INPUT
    bEnableSys            : BOOL;   (* Main system enable toggle *)
    bEmergencyStop        : BOOL;   (* Hardware E-Stop OK (Normally Closed loop) *)
    rGasLevel_CH4         : REAL;   (* Methane concentration (% LEL) *)
    rGasLevel_CO          : REAL;   (* Carbon Monoxide concentration (PPM) *)
    rAirflow_Feedback     : REAL;   (* Current airflow measured in shaft (m3/s) *)
    bPersonnelInZone      : BOOL;   (* True if personnel are detected in extraction zone *)
    iFanVFD_Status        : INT;    (* Fan Drive Status word: 0=Fault, 1=Ready, 2=Running *)
    rTemp_Ambient         : REAL;   (* Ambient temperature in deg C *)
END_VAR

VAR_OUTPUT
    bSystemReady          : BOOL;   (* Indicates all interlocks are clear and system is ready *)
    rFanVFD_Command       : REAL;   (* Speed command to main ventilation VFD (0.0 to 100.0 %) *)
    bEvacuationAlarm      : BOOL;   (* Trigger evacuation alarms and strobes *)
    bAuxExtractorEnable   : BOOL;   (* Enable auxiliary high-velocity gas extractors *)
    iActiveState          : INT;    (* Current active control state *)
    rFilteredCH4          : REAL;   (* Noise-filtered Methane concentration *)
END_VAR

VAR
    (* Internal State Machine *)
    iState                : INT := 0; 
    
    (* Timers *)
    tStartupDelay         : TON;
    tPurgeTimer           : TON;
    tSensorFaultTimer     : TON;
    
    (* Filter Buffers *)
    arrCH4_Buffer         : ARRAY[0..4] OF REAL := [0.0, 0.0, 0.0, 0.0, 0.0];
    rSumCH4               : REAL;
    iBufferIndex          : INT := 0;
    
    (* PID Variables *)
    rError                : REAL;
    rIntegral             : REAL := 0.0;
    rDerivative           : REAL;
    rLastError            : REAL := 0.0;
    rKp                   : REAL := 1.25;
    rKi                   : REAL := 0.15;
    rKd                   : REAL := 0.05;
    rDt                   : REAL := 0.1; (* 100ms scan cycle assumption *)
    
    (* Threshold Constants *)
    CH4_ALARM_LIMIT       : REAL := 1.5; (* % LEL Methane Evacuate Limit *)
    CO_ALARM_LIMIT        : REAL := 50.0; (* PPM CO Evacuate Limit *)
    AIRFLOW_TARGET_BASE   : REAL := 150.0; (* Base airflow m3/s *)
    
    (* Flags *)
    bCriticalGas          : BOOL;
    bSensorFault          : BOOL;
END_VAR

(* === MAIN LOGIC === *)

(* 1. Safety & Interlock Pre-Checks *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    rFanVFD_Command := 0.0;
    bEvacuationAlarm := TRUE; (* E-Stop triggers alarms *)
    bAuxExtractorEnable := FALSE;
    iState := 999; (* FAULT STATE *)
    RETURN;
END_IF;

(* 2. Sensor Noise Filtering - 5-Point Moving Average for CH4 *)
rSumCH4 := rSumCH4 - arrCH4_Buffer[iBufferIndex] + rGasLevel_CH4;
arrCH4_Buffer[iBufferIndex] := rGasLevel_CH4;
iBufferIndex := (iBufferIndex + 1) MOD 5;
rFilteredCH4 := rSumCH4 / 5.0;

(* Sensor Plausibility Check *)
bSensorFault := (rGasLevel_CH4 < -0.1) OR (rGasLevel_CO < -1.0) OR (rTemp_Ambient > 85.0);
tSensorFaultTimer(IN := bSensorFault, PT := T#2S);

IF tSensorFaultTimer.Q THEN
    bSystemReady := FALSE;
    iState := 999;
END_IF;

(* 3. Critical Gas Evaluation *)
bCriticalGas := (rFilteredCH4 >= CH4_ALARM_LIMIT) OR (rGasLevel_CO >= CO_ALARM_LIMIT);

IF bCriticalGas THEN
    bEvacuationAlarm := TRUE;
    IF NOT bPersonnelInZone THEN
        bAuxExtractorEnable := TRUE; (* Full extraction if zone is clear of personnel *)
    ELSE
        bAuxExtractorEnable := FALSE; (* Avoid stirring toxic dust/fumes if personnel are trapped *)
    END_IF;
ELSE
    bEvacuationAlarm := FALSE;
    bAuxExtractorEnable := FALSE;
END_IF;

(* 4. State Machine Control *)
CASE iState OF
    0: (* INIT / IDLE *)
        rFanVFD_Command := 0.0;
        bSystemReady := FALSE;
        IF bEnableSys AND (iFanVFD_Status = 1) AND NOT bCriticalGas THEN
            iState := 10;
        END_IF;

    10: (* PRE-STARTUP PURGE *)
        bSystemReady := TRUE;
        rFanVFD_Command := 30.0; (* 30% speed for initial purge *)
        tStartupDelay(IN := TRUE, PT := T#30S);
        
        IF tStartupDelay.Q THEN
            tStartupDelay(IN := FALSE);
            iState := 20;
        END_IF;
        
        IF NOT bEnableSys THEN
            tStartupDelay(IN := FALSE);
            iState := 0;
        END_IF;

    20: (* NORMAL OPERATION (PID ACTIVE) *)
        bSystemReady := TRUE;
        
        (* Calculate dynamic airflow target based on temperature and base requirement *)
        rError := (AIRFLOW_TARGET_BASE + (rTemp_Ambient * 0.5)) - rAirflow_Feedback;
        
        (* PID Calculation *)
        rIntegral := rIntegral + (rError * rDt);
        
        (* Anti-windup *)
        IF rIntegral > 50.0 THEN rIntegral := 50.0; END_IF;
        IF rIntegral < -50.0 THEN rIntegral := -50.0; END_IF;
        
        rDerivative := (rError - rLastError) / rDt;
        rFanVFD_Command := (rKp * rError) + (rKi * rIntegral) + (rKd * rDerivative) + 50.0; (* 50% baseline feed-forward *)
        
        rLastError := rError;
        
        (* Clamp Output *)
        IF rFanVFD_Command > 100.0 THEN
            rFanVFD_Command := 100.0;
        ELSIF rFanVFD_Command < 20.0 THEN
            rFanVFD_Command := 20.0; (* Minimum speed to prevent stall *)
        END_IF;

        IF bCriticalGas THEN
            iState := 30; (* Escalate to EMERGENCY *)
        END_IF;
        
        IF NOT bEnableSys THEN
            iState := 0;
        END_IF;

    30: (* EMERGENCY CASCADE EXTRACTION *)
        bSystemReady := FALSE;
        rFanVFD_Command := 100.0; (* Max ventilation *)
        
        IF NOT bCriticalGas THEN
            tPurgeTimer(IN := TRUE, PT := T#120S); (* Wait 2 mins after clear *)
            IF tPurgeTimer.Q THEN
                tPurgeTimer(IN := FALSE);
                iState := 20; (* Return to normal *)
            END_IF;
        ELSE
            tPurgeTimer(IN := FALSE);
        END_IF;

    999: (* FAULT STATE *)
        bSystemReady := FALSE;
        rFanVFD_Command := 0.0;
        IF NOT bSensorFault AND bEmergencyStop AND bEnableSys THEN
            iState := 0; (* Reset if conditions allow *)
        END_IF;
        
END_CASE;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
