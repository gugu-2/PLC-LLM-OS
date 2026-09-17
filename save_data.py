import json
import uuid

prompt = """<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Automated Commercial Semiconductor Cleanroom HEPA Filter Fan Unit (FFU) and Differential Pressure Synchronization**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Cleanroom_FFU_Sync\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
   record = {\"messages\": [{\"role\": \"user\", \"content\": prompt}, {\"role\": \"assistant\", \"content\": code}]}
   with open(f\"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json\", \"w\", encoding=\"utf-8\") as f:
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
6. REPLY with: EVOLUTION COMPLETE: Automated Commercial Semiconductor Cleanroom HEPA Filter Fan Unit (FFU) and Differential Pressure Synchronization

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.
</USER_REQUEST>"""

code = """```iec-st
FUNCTION_BLOCK FB_Cleanroom_FFU_Sync
VAR_INPUT
    bEnable                 : BOOL;     (* System global enable *)
    bEmergencyStop          : BOOL;     (* Emergency stop circuit OK (TRUE = OK) *)
    rRoomPressure_Pa        : REAL;     (* Measured differential pressure of cleanroom vs ambient (Pascals) *)
    rSupplyAirTemp_C        : REAL;     (* Supply air temperature (Celsius) *)
    rPlenumPressure_Pa      : REAL;     (* Pressure in the common FFU plenum (Pascals) *)
    rTargetPressure_Pa      : REAL;     (* Target cleanroom differential pressure (Pascals) *)
    rFFU_RPM_Feedback       : REAL;     (* Average FFU fan speed feedback (RPM) *)
    bDoorOpenInterlock      : BOOL;     (* TRUE if cleanroom access door is open *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* System is ready for operation *)
    rFFU_SpeedCmd_Pct       : REAL;     (* FFU speed command (0.0 to 100.0%) *)
    bPressureAlarm          : BOOL;     (* Differential pressure out of bounds alarm *)
    bFFU_Fault              : BOOL;     (* FFU mechanical or communication fault *)
    iOperatingState         : INT;      (* Current state machine step *)
    rFilteredPressure_Pa    : REAL;     (* Filtered room pressure for monitoring *)
END_VAR
VAR
    iState                  : INT := 0; (* State machine variable *)
    tStartupDelay           : TON;      (* Delay timer for startup sequence *)
    tAlarmDelay             : TON;      (* Delay timer to prevent nuisance pressure alarms *)
    
    (* Filter variables *)
    rAlpha                  : REAL := 0.1; (* Low-pass filter coefficient *)
    rPrevPressure_Pa        : REAL := 0.0;
    
    (* PID Controller variables *)
    rError                  : REAL := 0.0;
    rIntegral               : REAL := 0.0;
    rDerivative             : REAL := 0.0;
    rLastError              : REAL := 0.0;
    rKp                     : REAL := 2.5; (* Proportional gain *)
    rKi                     : REAL := 0.5; (* Integral gain *)
    rKd                     : REAL := 0.1; (* Derivative gain *)
    
    (* Safety limits *)
    rMaxSpeed_Pct           : REAL := 100.0;
    rMinSpeed_Pct           : REAL := 20.0;
    rMaxPressureDev_Pa      : REAL := 15.0; (* Max allowable pressure deviation before alarm *)
    
    bInitDone               : BOOL := FALSE;
END_VAR

(* === MAIN LOGIC === *)
IF NOT bInitDone THEN
    rPrevPressure_Pa := rRoomPressure_Pa;
    rFilteredPressure_Pa := rRoomPressure_Pa;
    bInitDone := TRUE;
END_IF;

(* Emergency Stop Handling *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    rFFU_SpeedCmd_Pct := 0.0;
    bPressureAlarm := TRUE;
    iState := 999; (* E-STOP State *)
    iOperatingState := iState;
    rIntegral := 0.0; (* Reset integral windup *)
    RETURN;
END_IF;

(* Input Filtering - Low Pass Filter for Room Pressure to remove sensor noise *)
rFilteredPressure_Pa := (rAlpha * rRoomPressure_Pa) + ((1.0 - rAlpha) * rPrevPressure_Pa);
rPrevPressure_Pa := rFilteredPressure_Pa;

(* Main State Machine *)
CASE iState OF
    0: (* IDLE / STANDBY *)
        bSystemReady := TRUE;
        rFFU_SpeedCmd_Pct := 0.0;
        bPressureAlarm := FALSE;
        IF bEnable AND NOT bDoorOpenInterlock THEN
            iState := 10;
        END_IF;

    10: (* STARTUP SEQUENCE *)
        bSystemReady := FALSE;
        rFFU_SpeedCmd_Pct := rMinSpeed_Pct; (* Start FFU at minimum speed *)
        tStartupDelay(IN := TRUE, PT := T#15S);
        
        IF tStartupDelay.Q THEN
            tStartupDelay(IN := FALSE);
            iState := 20; (* Move to active regulation *)
        END_IF;
        
        IF NOT bEnable THEN
            tStartupDelay(IN := FALSE);
            iState := 0;
        END_IF;

    20: (* ACTIVE PID REGULATION *)
        bSystemReady := TRUE;
        
        (* Calculate Error *)
        rError := rTargetPressure_Pa - rFilteredPressure_Pa;
        
        (* Door Open Interlock - Pause Integration, Maintain Speed *)
        IF bDoorOpenInterlock THEN
            rError := 0.0;
            (* Preemptively boost speed slightly to compensate for open door *)
            rFFU_SpeedCmd_Pct := rFFU_SpeedCmd_Pct + 10.0; 
            IF rFFU_SpeedCmd_Pct > rMaxSpeed_Pct THEN
                rFFU_SpeedCmd_Pct := rMaxSpeed_Pct;
            END_IF;
        ELSE
            (* PID Calculation *)
            rIntegral := rIntegral + (rError * rKi);
            
            (* Anti-windup clamping *)
            IF rIntegral > 50.0 THEN
                rIntegral := 50.0;
            ELSIF rIntegral < -50.0 THEN
                rIntegral := -50.0;
            END_IF;
            
            rDerivative := (rError - rLastError) * rKd;
            rLastError := rError;
            
            (* Final Control Output *)
            rFFU_SpeedCmd_Pct := (rError * rKp) + rIntegral + rDerivative;
            
            (* Output limits *)
            IF rFFU_SpeedCmd_Pct > rMaxSpeed_Pct THEN
                rFFU_SpeedCmd_Pct := rMaxSpeed_Pct;
            ELSIF rFFU_SpeedCmd_Pct < rMinSpeed_Pct THEN
                rFFU_SpeedCmd_Pct := rMinSpeed_Pct;
            END_IF;
        END_IF;
        
        (* Alarm Logic *)
        tAlarmDelay(IN := (ABS(rTargetPressure_Pa - rFilteredPressure_Pa) > rMaxPressureDev_Pa), PT := T#10S);
        IF tAlarmDelay.Q THEN
            bPressureAlarm := TRUE;
        ELSE
            bPressureAlarm := FALSE;
        END_IF;
        
        (* Return to idle if disabled *)
        IF NOT bEnable THEN
            iState := 0;
            rIntegral := 0.0;
            tAlarmDelay(IN := FALSE);
        END_IF;

    999: (* FAULT / E-STOP STATE *)
        bSystemReady := FALSE;
        rFFU_SpeedCmd_Pct := 0.0;
        IF bEmergencyStop AND bEnable THEN
            iState := 0; (* Reset sequence requires Enable cycle *)
        END_IF;

END_CASE;

iOperatingState := iState;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}

filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
