import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial Metal Wire Galvanizing Line Zinc Bath Temperature and Wiper Die Air Pressure**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_WireGalvanizing_Control\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Metal Wire Galvanizing Line Zinc Bath Temperature and Wiper Die Air Pressure

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_WireGalvanizing_Control
VAR_INPUT
    bEnable                 : BOOL;     (* Main system enable signal *)
    bEmergencyStop          : BOOL;     (* Safety interlock / Emergency Stop (Active LOW) *)
    rZincBathTemp_PT1       : REAL;     (* Temperature of Zinc Bath Sensor 1 [deg C] *)
    rZincBathTemp_PT2       : REAL;     (* Temperature of Zinc Bath Sensor 2 [deg C] *)
    rWiperDiePressure_FB    : REAL;     (* Feedback from Air Knife / Wiper Die Pressure [Bar] *)
    rLineSpeed_mps          : REAL;     (* Wire line speed [m/s] *)
    rTargetZincTemp         : REAL;     (* Target Zinc Bath Temperature [deg C] *)
    rTargetWiperPressure    : REAL;     (* Target Wiper Air Pressure [Bar] *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* System is ready and operating in bounds *)
    rZincHeaterOutput       : REAL;     (* Output to Zinc Bath Heater Controller [0.0 - 100.0%] *)
    rWiperValveOutput       : REAL;     (* Output to Wiper Air Proportional Valve [0.0 - 100.0%] *)
    bAlarmZincTemp          : BOOL;     (* High/Low alarm for Zinc bath temperature *)
    bAlarmWiperPressure     : BOOL;     (* High/Low alarm for Wiper die air pressure *)
    bGlobalFault            : BOOL;     (* Global fault indicator *)
END_VAR
VAR
    iState                  : INT := 0; (* Main State Machine *)
    rFilteredZincTemp       : REAL;     (* Noise-filtered Zinc Bath Temp *)
    rFilteredWiperPress     : REAL;     (* Noise-filtered Wiper Pressure *)
    
    (* Filter Constants *)
    rAlphaTemp              : REAL := 0.05;
    rAlphaPress             : REAL := 0.10;
    
    (* PID Variables for Zinc Bath *)
    rZincError              : REAL;
    rZincErrorPrev          : REAL;
    rZincIntegral           : REAL;
    rZincDerivative         : REAL;
    rKpZinc                 : REAL := 2.5;
    rKiZinc                 : REAL := 0.02;
    rKdZinc                 : REAL := 0.5;
    
    (* PID Variables for Wiper Pressure *)
    rWiperError             : REAL;
    rWiperErrorPrev         : REAL;
    rWiperIntegral          : REAL;
    rWiperDerivative        : REAL;
    rKpWiper                : REAL := 5.0;
    rKiWiper                : REAL := 0.1;
    rKdWiper                : REAL := 0.05;
    
    (* Timers *)
    tHeaterDelay            : TON;
    tFaultTimer             : TON;
    
    (* Safety limits *)
    MAX_ZINC_TEMP           : REAL := 480.0;
    MIN_ZINC_TEMP           : REAL := 430.0;
    MAX_WIPER_PRESS         : REAL := 8.0;
    
    bInitDone               : BOOL := FALSE;
END_VAR

(* === MAIN LOGIC === *)

(* Initialization *)
IF NOT bInitDone THEN
    rFilteredZincTemp := (rZincBathTemp_PT1 + rZincBathTemp_PT2) / 2.0;
    rFilteredWiperPress := rWiperDiePressure_FB;
    bInitDone := TRUE;
END_IF;

(* Emergency Stop & Safety Interlocks *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bGlobalFault := TRUE;
    bAlarmZincTemp := FALSE;
    bAlarmWiperPressure := FALSE;
    rZincHeaterOutput := 0.0;
    rWiperValveOutput := 0.0;
    iState := 0;
    RETURN;
END_IF;

(* Sensor Processing with Exponential Smoothing Filter *)
(* Average of two redundant sensors for zinc bath *)
rFilteredZincTemp := rAlphaTemp * ((rZincBathTemp_PT1 + rZincBathTemp_PT2) / 2.0) + (1.0 - rAlphaTemp) * rFilteredZincTemp;
rFilteredWiperPress := rAlphaPress * rWiperDiePressure_FB + (1.0 - rAlphaPress) * rFilteredWiperPress;

(* Diagnostics and Alarms *)
bAlarmZincTemp := (rFilteredZincTemp > MAX_ZINC_TEMP) OR (rFilteredZincTemp < MIN_ZINC_TEMP);
bAlarmWiperPressure := (rFilteredWiperPress > MAX_WIPER_PRESS);

IF bAlarmZincTemp OR bAlarmWiperPressure THEN
    tFaultTimer(IN := TRUE, PT := T#3S);
ELSE
    tFaultTimer(IN := FALSE);
END_IF;

IF tFaultTimer.Q THEN
    bGlobalFault := TRUE;
    iState := 99; (* Fault State *)
END_IF;

(* Main State Machine *)
CASE iState OF
    0: (* IDLE *)
        bSystemReady := FALSE;
        rZincHeaterOutput := 0.0;
        rWiperValveOutput := 0.0;
        bGlobalFault := FALSE;
        IF bEnable AND NOT bGlobalFault THEN
            iState := 10;
        END_IF;

    10: (* PRE-HEATING ZINC BATH *)
        (* PID Control for Zinc Bath Temp *)
        rZincError := rTargetZincTemp - rFilteredZincTemp;
        rZincIntegral := rZincIntegral + rZincError;
        (* Anti-windup for zinc heater *)
        IF rZincIntegral > 1000.0 THEN rZincIntegral := 1000.0; END_IF;
        IF rZincIntegral < -1000.0 THEN rZincIntegral := -1000.0; END_IF;
        
        rZincDerivative := rZincError - rZincErrorPrev;
        rZincErrorPrev := rZincError;
        
        rZincHeaterOutput := (rKpZinc * rZincError) + (rKiZinc * rZincIntegral) + (rKdZinc * rZincDerivative);
        
        IF rZincHeaterOutput > 100.0 THEN rZincHeaterOutput := 100.0; END_IF;
        IF rZincHeaterOutput < 0.0 THEN rZincHeaterOutput := 0.0; END_IF;
        
        tHeaterDelay(IN := (rZincError < 5.0 AND rZincError > -5.0), PT := T#10S);
        IF tHeaterDelay.Q THEN
            tHeaterDelay(IN := FALSE);
            iState := 20;
        END_IF;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    20: (* RUNNING / WIRE GALVANIZING *)
        bSystemReady := TRUE;
        
        (* Zinc Heater PID Maintenance *)
        rZincError := rTargetZincTemp - rFilteredZincTemp;
        rZincIntegral := rZincIntegral + rZincError;
        IF rZincIntegral > 1000.0 THEN rZincIntegral := 1000.0; END_IF;
        IF rZincIntegral < -1000.0 THEN rZincIntegral := -1000.0; END_IF;
        rZincDerivative := rZincError - rZincErrorPrev;
        rZincErrorPrev := rZincError;
        rZincHeaterOutput := (rKpZinc * rZincError) + (rKiZinc * rZincIntegral) + (rKdZinc * rZincDerivative);
        IF rZincHeaterOutput > 100.0 THEN rZincHeaterOutput := 100.0; END_IF;
        IF rZincHeaterOutput < 0.0 THEN rZincHeaterOutput := 0.0; END_IF;

        (* Wiper Die Air Pressure PID - Feedforward based on Line Speed *)
        rWiperError := (rTargetWiperPressure + (rLineSpeed_mps * 0.1)) - rFilteredWiperPress;
        rWiperIntegral := rWiperIntegral + rWiperError;
        IF rWiperIntegral > 200.0 THEN rWiperIntegral := 200.0; END_IF;
        IF rWiperIntegral < -200.0 THEN rWiperIntegral := -200.0; END_IF;
        rWiperDerivative := rWiperError - rWiperErrorPrev;
        rWiperErrorPrev := rWiperError;
        rWiperValveOutput := (rKpWiper * rWiperError) + (rKiWiper * rWiperIntegral) + (rKdWiper * rWiperDerivative);
        IF rWiperValveOutput > 100.0 THEN rWiperValveOutput := 100.0; END_IF;
        IF rWiperValveOutput < 0.0 THEN rWiperValveOutput := 0.0; END_IF;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    99: (* FAULT HANDLING *)
        bSystemReady := FALSE;
        rZincHeaterOutput := 0.0;
        rWiperValveOutput := 0.0;
        IF NOT bAlarmZincTemp AND NOT bAlarmWiperPressure AND bEnable THEN
            IF NOT bGlobalFault THEN
                iState := 0;
            END_IF;
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

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
