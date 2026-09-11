import os
import json
import uuid

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Advanced Industrial Scale Direct Air Capture (DAC) Amine Sorbent Contactor**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Low-temperature vacuum swing adsorption (VSA) cycle sequencing, monolithic amine-functionalized honeycomb structural thermal profiling, and atmospheric dew point steam regeneration). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_DAC_AmineContactor\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Advanced Industrial Scale Direct Air Capture (DAC) Amine Sorbent Contactor

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_DAC_AmineContactor
VAR_INPUT
    (* Physical Inputs *)
    bEnable                 : BOOL;     (* System enable signal *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal - E-Stop *)
    rInletAirTemp           : REAL;     (* Inlet atmospheric air temperature [degC] *)
    rInletAirRH             : REAL;     (* Inlet atmospheric relative humidity [%] *)
    rSorbentTemp            : REAL;     (* Monolithic honeycomb sorbent bed temperature [degC] *)
    rVacuumPressure         : REAL;     (* Chamber vacuum pressure [mbar absolute] *)
    rSteamFlowRate          : REAL;     (* Regeneration steam flow rate [kg/h] *)
    rCO2Concentration       : REAL;     (* Outlet CO2 concentration [ppm] *)
END_VAR
VAR_OUTPUT
    (* Physical Outputs *)
    bSystemReady            : BOOL;     (* System ready status *)
    rFanSpeedSetpoint       : REAL;     (* Contactor fan speed command [rpm] *)
    rVacuumValveCmd         : REAL;     (* Vacuum pump isolation valve command [% open] *)
    rSteamValveCmd          : REAL;     (* Regeneration steam control valve command [% open] *)
    bRegenCycleActive       : BOOL;     (* Status flag indicating regeneration in progress *)
    bAlarm                  : BOOL;     (* Fault alarm output *)
    iFaultCode              : INT;      (* Specific fault code for diagnostics *)
END_VAR
VAR
    (* Internal state variables *)
    iState                  : INT := 0; (* State machine step index *)
    tStateTimer             : TON;      (* Timer for state transitions and timeouts *)
    
    (* Filtered signals *)
    rSorbentTempFilt        : REAL;
    rVacuumPressureFilt     : REAL;
    
    (* Filter constants *)
    rAlphaTemp              : REAL := 0.05;
    rAlphaPress             : REAL := 0.1;
    
    (* Control parameters *)
    rTargetAdsorbTemp       : REAL := 25.0;  (* Optimal adsorption temp *)
    rMaxRegenTemp           : REAL := 115.0; (* Max allowable regeneration temp *)
    rTargetVacuum           : REAL := 150.0; (* Target vacuum for VSA [mbar] *)
    
    (* PI Controller for Steam *)
    rSteamError             : REAL;
    rSteamIntegral          : REAL;
    rSteamKp                : REAL := 2.5;
    rSteamKi                : REAL := 0.2;
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety Interlocks and E-Stop Processing *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bAlarm := TRUE;
    iFaultCode := 999; (* Critical Safety Trip *)
    
    (* Safe state enforcement *)
    rFanSpeedSetpoint := 0.0;
    rVacuumValveCmd := 0.0;
    rSteamValveCmd := 0.0;
    bRegenCycleActive := FALSE;
    iState := 0;
    RETURN;
END_IF;

(* 2. Sensor Noise Filtering (First-order IIR) *)
rSorbentTempFilt := (rAlphaTemp * rSorbentTemp) + ((1.0 - rAlphaTemp) * rSorbentTempFilt);
rVacuumPressureFilt := (rAlphaPress * rVacuumPressure) + ((1.0 - rAlphaPress) * rVacuumPressureFilt);

(* 3. General Fault Monitoring *)
IF rSorbentTempFilt > rMaxRegenTemp + 5.0 THEN
    bAlarm := TRUE;
    iFaultCode := 101; (* Thermal Runaway *)
    rSteamValveCmd := 0.0;
    iState := 0;
    RETURN;
END_IF;

(* 4. Main State Machine for DAC VSA Cycle *)
CASE iState OF
    0: (* IDLE & INITIALIZATION *)
        bSystemReady := TRUE;
        bRegenCycleActive := FALSE;
        rFanSpeedSetpoint := 0.0;
        rVacuumValveCmd := 0.0;
        rSteamValveCmd := 0.0;
        
        IF bEnable THEN
            bAlarm := FALSE;
            iFaultCode := 0;
            iState := 10;
            tStateTimer(IN := FALSE);
        END_IF;

    10: (* ADSORPTION PHASE - Atmospheric Air Flow *)
        (* Modulate fan speed based on inlet temperature to maintain contact time *)
        IF rInletAirTemp > 30.0 THEN
            rFanSpeedSetpoint := 1500.0;
        ELSE
            rFanSpeedSetpoint := 1200.0;
        END_IF;
        
        (* Monitor CO2 breakthrough to trigger regeneration *)
        IF rCO2Concentration > 450.0 THEN
            (* Sorbent saturated, prepare for regeneration *)
            tStateTimer(IN := TRUE, PT := T#10S);
            IF tStateTimer.Q THEN
                iState := 20;
                tStateTimer(IN := FALSE);
            END_IF;
        ELSE
            tStateTimer(IN := FALSE);
        END_IF;

    20: (* EVACUATION PHASE - Draw Vacuum *)
        bRegenCycleActive := TRUE;
        rFanSpeedSetpoint := 0.0; (* Stop atmospheric air flow *)
        
        (* Open vacuum isolation valve ramped *)
        rVacuumValveCmd := MIN(rVacuumValveCmd + 0.5, 100.0);
        
        IF rVacuumPressureFilt <= rTargetVacuum THEN
            iState := 30;
            rSteamIntegral := 0.0; (* Reset controller for next phase *)
        END_IF;
        
        (* Timeout protection *)
        tStateTimer(IN := TRUE, PT := T#5M);
        IF tStateTimer.Q THEN
            bAlarm := TRUE;
            iFaultCode := 201; (* Vacuum draw failed *)
            iState := 0;
        END_IF;

    30: (* STEAM REGENERATION & THERMAL SWING *)
        (* PI Control of steam valve to reach target regeneration temperature *)
        rSteamError := 105.0 - rSorbentTempFilt;
        rSteamIntegral := rSteamIntegral + (rSteamError * 0.1); (* 100ms assumed cycle *)
        
        (* Anti-windup *)
        IF rSteamIntegral > 50.0 THEN rSteamIntegral := 50.0; END_IF;
        IF rSteamIntegral < 0.0 THEN rSteamIntegral := 0.0; END_IF;
        
        rSteamValveCmd := (rSteamKp * rSteamError) + (rSteamKi * rSteamIntegral);
        
        (* Clamp output *)
        IF rSteamValveCmd > 100.0 THEN rSteamValveCmd := 100.0; END_IF;
        IF rSteamValveCmd < 0.0 THEN rSteamValveCmd := 0.0; END_IF;
        
        (* Hold phase once temperature reached *)
        IF rSorbentTempFilt >= 100.0 THEN
            tStateTimer(IN := TRUE, PT := T#15M);
            IF tStateTimer.Q THEN
                iState := 40;
                tStateTimer(IN := FALSE);
            END_IF;
        ELSE
            tStateTimer(IN := FALSE);
        END_IF;

    40: (* COOLING & REPRESSURIZATION *)
        rSteamValveCmd := 0.0;
        rVacuumValveCmd := MAX(rVacuumValveCmd - 1.0, 0.0); (* Ramp close vacuum *)
        
        (* Induce cooling via low-speed ambient air *)
        rFanSpeedSetpoint := 500.0;
        
        IF rSorbentTempFilt <= rTargetAdsorbTemp + 5.0 AND rVacuumValveCmd = 0.0 THEN
            bRegenCycleActive := FALSE;
            IF NOT bEnable THEN
                iState := 0;
            ELSE
                iState := 10; (* Return to Adsorption *)
            END_IF;
        END_IF;

    ELSE
        (* Invalid state catch *)
        iState := 0;
END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
