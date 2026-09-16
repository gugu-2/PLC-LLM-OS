import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial Scale Animal Feed Pelletizing Die Roll Pressure and Steam Conditioning**

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
   code = \"\"\"```iec-st\nFUNCTION_BLOCK FB_FeedPelletizer_Conditioning\n//...\nEND_FUNCTION_BLOCK\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Scale Animal Feed Pelletizing Die Roll Pressure and Steam Conditioning

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_FeedPelletizer_Conditioning
VAR_INPUT
    (* Required: at least 4-8 physical inputs with types and comments *)
    bEnable               : BOOL;   (* System enable command *)
    bEmergencyStop        : BOOL;   (* Master safety relay OK signal, active high = OK *)
    rSteamTemp            : REAL;   (* Conditioning steam temperature [deg C] *)
    rDiePressure_Left     : REAL;   (* Hydraulic pressure on left die roll [Bar] *)
    rDiePressure_Right    : REAL;   (* Hydraulic pressure on right die roll [Bar] *)
    rMainMotorLoad        : REAL;   (* Main pellet mill motor load [Amps] *)
    rMoistureFeed         : REAL;   (* Mash feed moisture content [%] *)
    rTargetPressure       : REAL;   (* Setpoint for die roll pressure [Bar] *)
END_VAR
VAR_OUTPUT
    (* Required: at least 3-6 outputs with types and comments *)
    bSystemReady          : BOOL;   (* Interlocks satisfied, ready for operation *)
    rSteamValveCommand    : REAL;   (* Steam proportional valve output [0-100%] *)
    rDiePressureCommand   : REAL;   (* Roll pressure hydraulic servo command [0-100%] *)
    bAlarm                : BOOL;   (* Critical system fault active *)
    iFaultCode            : INT;    (* Active fault diagnostic code *)
    bMainMotorEnable      : BOOL;   (* Run permissive to main pelletizing motor *)
END_VAR
VAR
    (* Internal State and Timers *)
    iState                : INT := 0; 
    tSteamWarmupTimer     : TON;
    tPressureDwellTimer   : TON;
    tFaultDelay           : TON;
    
    (* Filtering arrays for hydraulic pressure noise mitigation *)
    rPressureLeft_Array   : ARRAY[0..4] OF REAL;
    rPressureRight_Array  : ARRAY[0..4] OF REAL;
    rFilteredPressLeft    : REAL;
    rFilteredPressRight   : REAL;
    iFilterIdx            : INT := 0;
    
    (* PID state variables for Steam Conditioning Control *)
    rSteamError           : REAL;
    rSteamIntegral        : REAL;
    rSteamDerivative      : REAL;
    rSteamPrevError       : REAL;
    
    (* PID Tuning Parameters for Steam *)
    rKp_Steam             : REAL := 2.85;
    rKi_Steam             : REAL := 0.12;
    rKd_Steam             : REAL := 0.045;
    
    rPressureAvg          : REAL;
    rPressureError        : REAL;
END_VAR

(* === MAIN LOGIC === *)
(* 1. Multi-layered Safety Interlocks and Fault Handling *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bMainMotorEnable := FALSE;
    rSteamValveCommand := 0.0;
    rDiePressureCommand := 0.0;
    bAlarm := TRUE;
    iFaultCode := 999; (* FATAL: E-STOP Active - Immediate safe state *)
    iState := 0;
    RETURN;
END_IF;

(* 2. Sensor Noise Filtering - 5-Point Moving Average for Die Roll Pressures *)
rPressureLeft_Array[iFilterIdx]  := rDiePressure_Left;
rPressureRight_Array[iFilterIdx] := rDiePressure_Right;

rFilteredPressLeft := (rPressureLeft_Array[0] + rPressureLeft_Array[1] + rPressureLeft_Array[2] + 
                       rPressureLeft_Array[3] + rPressureLeft_Array[4]) / 5.0;
rFilteredPressRight:= (rPressureRight_Array[0] + rPressureRight_Array[1] + rPressureRight_Array[2] + 
                       rPressureRight_Array[3] + rPressureRight_Array[4]) / 5.0;

iFilterIdx := (iFilterIdx + 1) MOD 5;

(* Calculate averaged symmetric pressure for control algorithms *)
rPressureAvg := (rFilteredPressLeft + rFilteredPressRight) / 2.0;

(* 3. Hard Safety Envelope - Over-pressure mechanical interlock *)
IF rPressureAvg > 280.0 THEN (* 280 Bar absolute physical limit for die integrity *)
    bAlarm := TRUE;
    iFaultCode := 101; (* CRITICAL: Over-pressure detected, entering fault containment *)
    iState := 99;
END_IF;

(* 4. Main Process Control State Machine *)
CASE iState OF
    0: (* IDLE / READY TO START *)
        bSystemReady := TRUE;
        bMainMotorEnable := FALSE;
        rSteamValveCommand := 0.0;
        rDiePressureCommand := 0.0;
        IF bEnable THEN
            bSystemReady := FALSE;
            iState := 10;
        END_IF;
        
    10: (* WARMUP: STEAM CONDITIONING STABILIZATION *)
        (* Advanced PID calculation for optimal mash gelatinization *)
        rSteamError := 85.0 - rSteamTemp; (* Target 85 deg C for optimal starch breakdown *)
        rSteamIntegral := rSteamIntegral + rSteamError;
        rSteamDerivative := rSteamError - rSteamPrevError;
        
        rSteamValveCommand := (rKp_Steam * rSteamError) + (rKi_Steam * rSteamIntegral) + (rKd_Steam * rSteamDerivative);
        rSteamPrevError := rSteamError;
        
        (* Anti-Windup / Valve Command Clamping *)
        IF rSteamValveCommand > 100.0 THEN 
            rSteamValveCommand := 100.0; 
            rSteamIntegral := rSteamIntegral - rSteamError; (* Halt integral accumulation *)
        ELSIF rSteamValveCommand < 0.0 THEN 
            rSteamValveCommand := 0.0; 
            rSteamIntegral := 0.0; 
        END_IF;
        
        (* Wait for temperature stabilization using timer hysteresis *)
        tSteamWarmupTimer(IN := (rSteamTemp >= 83.5 AND rSteamTemp <= 86.5), PT := T#20S);
        IF tSteamWarmupTimer.Q THEN
            tSteamWarmupTimer(IN := FALSE);
            iState := 20;
        END_IF;
        
    20: (* RAMP-UP: PRESSURIZE DIE ROLLS *)
        rPressureError := rTargetPressure - rPressureAvg;
        rDiePressureCommand := rDiePressureCommand + (rPressureError * 0.15); (* Proportional pressure ramp *)
        
        IF rDiePressureCommand > 100.0 THEN rDiePressureCommand := 100.0; END_IF;
        IF rDiePressureCommand < 0.0 THEN rDiePressureCommand := 0.0; END_IF;
        
        (* Verify hydraulic pressure matches setpoint before introducing load *)
        tPressureDwellTimer(IN := (ABS(rPressureError) < 3.5), PT := T#8S);
        IF tPressureDwellTimer.Q THEN
            tPressureDwellTimer(IN := FALSE);
            iState := 30;
        END_IF;
        
    30: (* NORMAL OPERATION / ACTIVE PELLETIZING *)
        bMainMotorEnable := TRUE;
        
        (* Real-time adaptive slip-control load shedding *)
        IF rMainMotorLoad > 400.0 THEN (* Nearing main motor thermal overload *)
            rDiePressureCommand := rDiePressureCommand - 2.5; (* Back off pressure dynamically to prevent slip/jam *)
        END_IF;
        
        IF NOT bEnable THEN
            iState := 40;
        END_IF;
        
    40: (* CONTROLLED SHUTDOWN SEQUENCE *)
        bMainMotorEnable := FALSE;
        rSteamValveCommand := 0.0; (* Secure steam immediately *)
        rDiePressureCommand := rDiePressureCommand - 3.0; (* Controlled pressure bleed-off *)
        
        IF rDiePressureCommand <= 0.0 THEN
            rDiePressureCommand := 0.0;
            iState := 0;
        END_IF;
        
    99: (* FAULT CONTAINMENT STATE *)
        bMainMotorEnable := FALSE;
        rSteamValveCommand := 0.0;
        rDiePressureCommand := 0.0; (* Release all roll pressure to clear blockages *)
        
        (* Fault reset mechanism *)
        IF NOT bEnable AND bEmergencyStop THEN 
            bAlarm := FALSE;
            iFaultCode := 0;
            iState := 0;
        END_IF;
        
END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump({"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}, f, ensure_ascii=False)
print(f"Saved to {filename}")
