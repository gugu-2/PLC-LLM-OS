import os, json, uuid

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial Scale Sugar Refinery Vacuum Pan Crystallization and Brix Concentration**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_SugarRefinery_VacuumPan\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Scale Sugar Refinery Vacuum Pan Crystallization and Brix Concentration

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_VacuumPan_Crystallization_Control
(* ==============================================================================
   Block Name    : FB_VacuumPan_Crystallization_Control
   Description   : Advanced Industrial Scale Sugar Refinery Vacuum Pan Controller.
                   Manages the highly non-linear Brix concentration and
                   supersaturation process during sugar crystallization. 
                   Includes advanced PID control, multi-layer safety interlocks, 
                   Moving Average filters for sensor noise, and state-machine 
                   driven batch execution.
   ============================================================================== *)
VAR_INPUT
    bEnable                 : BOOL;     (* System global enable signal *)
    bEmergencyStop          : BOOL;     (* E-Stop/Safety relay OK signal (Active HIGH = OK) *)
    rBrixTransmitter        : REAL;     (* Raw Brix measurement [%] *)
    rPanPressure            : REAL;     (* Vacuum pan internal pressure [bar] *)
    rMassecuiteLevel        : REAL;     (* Massecuite level in the pan [m] *)
    rSteamValveFeedback     : REAL;     (* Steam valve position feedback [0-100%] *)
    bSeedInjectionCmd       : BOOL;     (* Operator/Supervisory command for seed injection *)
    rTargetBrix             : REAL;     (* Setpoint for final Brix concentration [%] *)
END_VAR

VAR_OUTPUT
    bSystemReady            : BOOL;     (* Indicates system is initialized and ready *)
    bBatchComplete          : BOOL;     (* Batch has reached target Brix and is ready to strike *)
    rSteamValveCmd          : REAL;     (* Commanded steam valve position [0-100%] *)
    rVacuumPumpSpeed        : REAL;     (* Commanded vacuum pump speed [0-100%] *)
    bSeedInjectionValve     : BOOL;     (* Command to open the seed injection valve *)
    bAlarm                  : BOOL;     (* Critical alarm output (pressure, E-stop) *)
    iCurrentState           : INT;      (* Current step in the crystallization sequence *)
END_VAR

VAR
    (* Internal States and Timers *)
    iState                  : INT := 0;
    tSeedInjectionTimer     : TON;
    tStabilizationTimer     : TON;
    
    (* Filtering *)
    rFilteredBrix           : REAL := 0.0;
    rBrixFilterAlpha        : REAL := 0.1; (* Exponential smoothing factor *)
    
    (* PID Control Variables for Steam *)
    rSteamKp                : REAL := 2.5;
    rSteamKi                : REAL := 0.05;
    rSteamKd                : REAL := 0.1;
    rSteamError             : REAL := 0.0;
    rSteamLastError         : REAL := 0.0;
    rSteamIntegral          : REAL := 0.0;
    rSteamDerivative        : REAL := 0.0;
    
    (* Safety limits *)
    rMaxPressure            : REAL := 1.5; (* Max safe pressure [bar] *)
    rMaxLevel               : REAL := 10.0; (* Max pan level [m] *)
END_VAR

(* === MAIN LOGIC === *)

(* 1. Safety Interlocks & E-Stop *)
IF NOT bEmergencyStop OR (rPanPressure > rMaxPressure) OR (rMassecuiteLevel > rMaxLevel) THEN
    bSystemReady := FALSE;
    bBatchComplete := FALSE;
    rSteamValveCmd := 0.0;
    rVacuumPumpSpeed := 0.0;
    bSeedInjectionValve := FALSE;
    bAlarm := TRUE;
    iState := 999; (* FAULT STATE *)
    iCurrentState := iState;
    RETURN;
END_IF;

bAlarm := FALSE;

(* 2. Sensor Filtering *)
(* Apply Exponential Moving Average to smooth noisy Brix readings *)
rFilteredBrix := (rBrixFilterAlpha * rBrixTransmitter) + ((1.0 - rBrixFilterAlpha) * rFilteredBrix);

(* 3. State Machine for Crystallization Batch Process *)
CASE iState OF
    0: (* IDLE & INITIALIZATION *)
        bSystemReady := TRUE;
        bBatchComplete := FALSE;
        rSteamValveCmd := 0.0;
        rVacuumPumpSpeed := 0.0;
        bSeedInjectionValve := FALSE;
        
        IF bEnable THEN
            iState := 10;
        END_IF;

    10: (* CHARGING: Bring pan to initial vacuum and fill with liquor *)
        rVacuumPumpSpeed := 100.0; (* Full vacuum *)
        
        IF rPanPressure < 0.2 THEN (* Vacuum established *)
            iState := 20;
        END_IF;

    20: (* CONCENTRATION: Evaporate water until supersaturation is reached *)
        (* PID Control for Steam based on Brix progression *)
        rSteamError := (rTargetBrix * 0.8) - rFilteredBrix; (* Initial concentration target before seeding *)
        
        (* Anti-windup for integral *)
        IF rSteamValveCmd > 0.0 AND rSteamValveCmd < 100.0 THEN
            rSteamIntegral := rSteamIntegral + rSteamError;
        END_IF;
        
        rSteamDerivative := rSteamError - rSteamLastError;
        rSteamValveCmd := (rSteamKp * rSteamError) + (rSteamKi * rSteamIntegral) + (rSteamKd * rSteamDerivative);
        rSteamLastError := rSteamError;
        
        (* Clamp steam valve output *)
        IF rSteamValveCmd > 100.0 THEN rSteamValveCmd := 100.0; END_IF;
        IF rSteamValveCmd < 0.0 THEN rSteamValveCmd := 0.0; END_IF;

        IF bSeedInjectionCmd THEN
            iState := 30;
        END_IF;

    30: (* SEEDING: Inject sugar seeds to start crystallization *)
        bSeedInjectionValve := TRUE;
        tSeedInjectionTimer(IN := TRUE, PT := T#15S);
        
        IF tSeedInjectionTimer.Q THEN
            bSeedInjectionValve := FALSE;
            tSeedInjectionTimer(IN := FALSE);
            iState := 40;
        END_IF;

    40: (* GROWING: Controlled boiling to grow crystals to target Brix *)
        (* Advanced PID to maintain optimal supersaturation via Brix *)
        rSteamError := rTargetBrix - rFilteredBrix;
        
        IF rSteamValveCmd > 0.0 AND rSteamValveCmd < 100.0 THEN
            rSteamIntegral := rSteamIntegral + rSteamError;
        END_IF;
        
        rSteamDerivative := rSteamError - rSteamLastError;
        rSteamValveCmd := (rSteamKp * rSteamError) + (rSteamKi * rSteamIntegral) + (rSteamKd * rSteamDerivative);
        rSteamLastError := rSteamError;
        
        IF rSteamValveCmd > 100.0 THEN rSteamValveCmd := 100.0; END_IF;
        IF rSteamValveCmd < 0.0 THEN rSteamValveCmd := 0.0; END_IF;

        IF rFilteredBrix >= rTargetBrix THEN
            tStabilizationTimer(IN := TRUE, PT := T#30S);
            IF tStabilizationTimer.Q THEN
                iState := 50;
            END_IF;
        ELSE
            tStabilizationTimer(IN := FALSE);
        END_IF;

    50: (* STRIKE / BATCH COMPLETE *)
        bBatchComplete := TRUE;
        rSteamValveCmd := 0.0;
        rVacuumPumpSpeed := 0.0;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;
        
    999: (* FAULT / RESET *)
        bSystemReady := FALSE;
        IF NOT bEmergencyStop THEN
            (* Wait for operator to clear fault and cycle enable *)
            IF NOT bEnable THEN
                iState := 0;
            END_IF;
        END_IF;

END_CASE;

iCurrentState := iState;

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
