import json, uuid, os
prompt = """<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Commercial Ski Resort Automated Snowmaking Pump House Wet Bulb Temperature and Nucleator Sync**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Snowmaking_PumpHouse\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Commercial Ski Resort Automated Snowmaking Pump House Wet Bulb Temperature and Nucleator Sync

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.
</USER_REQUEST>"""

code = """```iec-st
FUNCTION_BLOCK FB_Snowmaking_PumpHouse_Nucleator_Sync
(* 
    LUMINA AI CLOUD SWARM - ELITE AUTOMATION ARCHITECT 
    DOMAIN: Commercial Ski Resort Automated Snowmaking Pump House Wet Bulb Temperature and Nucleator Sync
    DESCRIPTION: Highly advanced control system for snowmaking, incorporating wet-bulb temperature 
                 calculations, nucleator water-air ratio syncing, pump pressure regulation via PID, 
                 and extreme weather/freeze protection interlocks.
*)
VAR_INPUT
    bEnableSystem          : BOOL;     (* System master enable signal from SCADA *)
    bEmergencyStop         : BOOL;     (* Safety circuit OK / E-Stop (Active High = OK) *)
    rAmbientTemp           : REAL;     (* Ambient Dry Bulb Temperature [deg C] *)
    rRelativeHumidity      : REAL;     (* Relative Humidity [%] 0.0 to 100.0 *)
    rWaterPressurePV       : REAL;     (* Current water manifold pressure [bar] *)
    rAirPressurePV         : REAL;     (* Current air compressor pressure [bar] *)
    bFlowSwitchWater       : BOOL;     (* Water flow confirmed (safety interlock) *)
    bFlowSwitchAir         : BOOL;     (* Air flow confirmed (safety interlock) *)
END_VAR

VAR_OUTPUT
    bSystemReady           : BOOL;     (* Overall system ready status *)
    bSnowGunsEnabled       : BOOL;     (* Permission to fire snow guns *)
    rWaterPumpCmd          : REAL;     (* VFD frequency command for water pump [Hz, 0-60] *)
    rAirCompressorCmd      : REAL;     (* VFD frequency command for air compressor [Hz, 0-60] *)
    rNucleatorRatioCmd     : REAL;     (* Nucleator air-to-water mixture ratio command *)
    bFreezeWarning         : BOOL;     (* Impending freeze damage warning (drain required) *)
    iFaultCode             : INT;      (* 0=OK, >0=Fault Code *)
END_VAR

VAR
    (* Internal State and State Machine Variables *)
    iState                 : INT := 0; (* 0: IDLE, 10: PRE_START, 20: WARMUP, 30: ACTIVE_CONTROL, 99: FAULT *)
    rWetBulbTemp           : REAL;     (* Calculated Wet Bulb Temperature [deg C] *)
    rTargetWaterPressure   : REAL;     (* Target water pressure based on wet-bulb [bar] *)
    
    (* Timers and Filtering *)
    tStartupTimer          : TON;
    tFaultDelay            : TON;
    tFreezeDwell           : TON;
    
    (* PID Controllers (Simulated with manual state here for structural rigor) *)
    rWaterErr              : REAL;
    rWaterErrPrev          : REAL;
    rWaterIntegral         : REAL;
    rKpWater               : REAL := 2.5;
    rKiWater               : REAL := 0.15;
    rKdWater               : REAL := 0.05;
    
    (* Filtering / Smoothing *)
    rFilteredAmbient       : REAL := 0.0;
    rFilteredRH            : REAL := 0.0;
    rAlpha                 : REAL := 0.1; (* Exponential moving average factor *)
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety Interlocks and Fast Fault Detection *)
IF NOT bEmergencyStop THEN
    bSystemReady     := FALSE;
    bSnowGunsEnabled := FALSE;
    rWaterPumpCmd    := 0.0;
    rAirCompressorCmd:= 0.0;
    iState           := 99;
    iFaultCode       := 1001; (* E-Stop Active *)
    RETURN;
END_IF;

(* 2. Sensor Filtering *)
(* Exponential moving average for noise rejection on critical atmospheric sensors *)
rFilteredAmbient := (rAmbientTemp * rAlpha) + (rFilteredAmbient * (1.0 - rAlpha));
rFilteredRH      := (rRelativeHumidity * rAlpha) + (rFilteredRH * (1.0 - rAlpha));

(* 3. Wet Bulb Temperature Approximation (Stull Equation for standard atmospheric pressure) *)
(* Note: Extremely robust empirical formula for wet-bulb calculation used in high-end psychrometrics *)
rWetBulbTemp := rFilteredAmbient * ATAN(0.151977 * SQRT(rFilteredRH + 8.313659)) + 
                ATAN(rFilteredAmbient + rFilteredRH) - ATAN(rFilteredRH - 1.676331) + 
                (0.00391838 * EXP(1.5 * LN(rFilteredRH))) * ATAN(0.023101 * rFilteredRH) - 4.686035;

(* 4. Freeze Protection and Warning *)
IF rFilteredAmbient < -20.0 THEN
    bFreezeWarning := TRUE;
    tFreezeDwell(IN := TRUE, PT := T#10S);
    IF tFreezeDwell.Q THEN
        (* Extreme cold can damage piping if flow stops, initiate forced shutdown if not active *)
        IF iState <> 30 THEN
            iState := 99;
            iFaultCode := 2002; (* Extreme cold, system not flowing - force drain state (external) *)
        END_IF;
    END_IF;
ELSE
    bFreezeWarning := FALSE;
    tFreezeDwell(IN := FALSE, PT := T#10S);
END_IF;

(* 5. Core State Machine *)
CASE iState OF
    0: (* IDLE *)
        bSystemReady     := TRUE;
        bSnowGunsEnabled := FALSE;
        rWaterPumpCmd    := 0.0;
        rAirCompressorCmd:= 0.0;
        
        IF bEnableSystem AND (rWetBulbTemp < -2.5) THEN
            (* Only start if wet bulb allows marginal snow quality (-2.5C WB threshold) *)
            iState := 10;
        END_IF;
        
    10: (* PRE_START / PURGE *)
        (* Start air compressor to purge lines and nucleators before introducing water *)
        rAirCompressorCmd := 30.0; (* 50% power purge *)
        tStartupTimer(IN := TRUE, PT := T#15S);
        
        IF tStartupTimer.Q AND bFlowSwitchAir THEN
            tStartupTimer(IN := FALSE);
            iState := 20;
        ELSIF tStartupTimer.Q AND NOT bFlowSwitchAir THEN
            iState := 99;
            iFaultCode := 3001; (* Air Purge Failed *)
        END_IF;

    20: (* WARMUP / WATER INTRO *)
        (* Ramp water pump to initial prime level *)
        rWaterPumpCmd := 20.0;
        tStartupTimer(IN := TRUE, PT := T#10S);
        
        IF tStartupTimer.Q AND bFlowSwitchWater THEN
            tStartupTimer(IN := FALSE);
            iState := 30;
        ELSIF tStartupTimer.Q AND NOT bFlowSwitchWater THEN
            iState := 99;
            iFaultCode := 4001; (* Water Prime Failed *)
        END_IF;

    30: (* ACTIVE_CONTROL / DYNAMIC PID & NUCLEATOR SYNC *)
        bSnowGunsEnabled := TRUE;
        
        (* Calculate dynamic target pressure based on Wet-Bulb *)
        (* Colder WB = More water capacity = Higher Pressure Target *)
        IF rWetBulbTemp <= -10.0 THEN
            rTargetWaterPressure := 35.0; (* MAX bar for deep cold *)
        ELSIF rWetBulbTemp > -10.0 AND rWetBulbTemp <= -2.5 THEN
            (* Linear interpolation between 20 bar (-2.5C) and 35 bar (-10C) *)
            rTargetWaterPressure := 20.0 + ((rWetBulbTemp + 2.5) / -7.5) * 15.0;
        ELSE
            (* Marginal conditions, idle back to prevent slush *)
            rTargetWaterPressure := 15.0; 
            IF rWetBulbTemp > -1.0 THEN
                (* Conditions degraded too far, abort snowmaking *)
                iState := 0;
            END_IF;
        END_IF;

        (* Execute Water Pressure PID Iteration *)
        rWaterErr := rTargetWaterPressure - rWaterPressurePV;
        rWaterIntegral := rWaterIntegral + (rWaterErr * 0.1); (* Assuming 100ms cycle simulation *)
        (* Anti-windup limit *)
        IF rWaterIntegral > 30.0 THEN rWaterIntegral := 30.0; END_IF;
        IF rWaterIntegral < 0.0 THEN rWaterIntegral := 0.0; END_IF;
        
        rWaterPumpCmd := (rKpWater * rWaterErr) + (rKiWater * rWaterIntegral) + (rKdWater * (rWaterErr - rWaterErrPrev));
        rWaterErrPrev := rWaterErr;
        
        (* Output Clamping *)
        IF rWaterPumpCmd > 60.0 THEN rWaterPumpCmd := 60.0; END_IF;
        IF rWaterPumpCmd < 15.0 THEN rWaterPumpCmd := 15.0; END_IF;

        (* Nucleator Ratio Syncing *)
        (* Nucleators require more air relative to water in marginal (warmer) conditions *)
        IF rWetBulbTemp > -4.0 THEN
            rNucleatorRatioCmd := 0.8; (* High Air/Water Ratio *)
            rAirCompressorCmd := 55.0;
        ELSE
            rNucleatorRatioCmd := 0.3; (* Low Air/Water Ratio (Max Water flow) *)
            rAirCompressorCmd := 40.0;
        END_IF;

        (* Stop Condition *)
        IF NOT bEnableSystem THEN
            iState := 0;
        END_IF;

    99: (* FAULT STATE *)
        bSystemReady := FALSE;
        bSnowGunsEnabled := FALSE;
        rWaterPumpCmd := 0.0;
        rAirCompressorCmd := 0.0;
        rNucleatorRatioCmd := 1.0; (* Full air to clear nozzles upon fault *)
        
        (* Require manual reset by dropping enable signal *)
        IF NOT bEnableSystem THEN
            iFaultCode := 0;
            iState := 0;
        END_IF;
        
END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print("Saved")
