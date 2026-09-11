import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Food-Grade Supercritical Fluid Extraction (SFE) Vessel**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., CO2 solvent density-pressure supercritical curve tracking (73 atm, 31°C), continuous botanical matrix feed lock-hopper pressure cascading, and cyclonic separator extract recovery). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_SupercriticalExtraction\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Food-Grade Supercritical Fluid Extraction (SFE) Vessel

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_SFE_VesselControl
(*
    =============================================================================
    BLOCK NAME: FB_SFE_VesselControl
    DESCRIPTION: High-precision control of Food-Grade Supercritical Fluid
                 Extraction (SFE) using CO2 solvent. Tracks density-pressure 
                 supercritical curve (target >73 atm, >31°C), manages continuous 
                 botanical matrix feed lock-hopper pressure cascading, and cyclonic 
                 separator extract recovery.
    AUTHOR: 40-Year Senior PLC Automation Architect
    =============================================================================
*)
VAR_INPUT
    (* Essential Physical Inputs *)
    bEnable                 : BOOL;     (* Main system enable command *)
    bEmergencyStop_OK       : BOOL;     (* Hardware safety circuit healthy (TRUE = Safe) *)
    rVesselPressure_Bar     : REAL;     (* Extraction vessel pressure transmitter (Bar) *)
    rVesselTemp_C           : REAL;     (* Extraction vessel RTD temperature (Deg C) *)
    rCO2FlowRate_kg_hr      : REAL;     (* Supercritical CO2 mass flow rate (kg/hr) *)
    bLockHopperReady        : BOOL;     (* Lock-hopper interlock: ready for pressure cascade *)
    rCyclonicSeparatorLevel : REAL;     (* Extract recovery level in cyclonic separator (0-100%) *)
END_VAR

VAR_OUTPUT
    (* Actuators & Status *)
    bSystemReady            : BOOL;     (* System is initialized and safe for operation *)
    rCO2PumpSpeed_Ref       : REAL;     (* VFD speed reference for high-pressure CO2 pump (%) *)
    rHeaterPower_Ref        : REAL;     (* SCR power reference for vessel heating jacket (%) *)
    bExtractDischargeValve  : BOOL;     (* Command to open cyclonic separator discharge valve *)
    bCascadeValveOpen       : BOOL;     (* Open lock-hopper pressure equalization valve *)
    bCriticalAlarm          : BOOL;     (* Critical process deviation or safety fault *)
    iOperationState         : INT;      (* Current state machine index for HMI display *)
END_VAR

VAR
    (* Internal State Variables *)
    iState                  : INT := 0; (* Internal state machine *)
    tStartupDelay           : TON;      (* Initialization timer *)
    tExtractDischargeTimer  : TON;      (* Duration for cyclonic extract discharge *)
    
    (* Process Setpoints *)
    rTargetPressure         : REAL := 74.0; (* supercritical CO2 target pressure (Bar), ~73 atm *)
    rTargetTemp             : REAL := 31.5; (* supercritical CO2 target temp (Deg C) *)
    
    (* PID Controllers (Conceptual representations) *)
    rPressureError          : REAL;
    rTempError              : REAL;
    
    (* Anti-Windup / Integral accumulators *)
    rPressureIntegral       : REAL := 0.0;
    rTempIntegral           : REAL := 0.0;
    
    (* Proportional Gains *)
    Kp_Press                : REAL := 2.5;
    Kp_Temp                 : REAL := 4.0;
    Ki_Press                : REAL := 0.05;
    Ki_Temp                 : REAL := 0.1;
END_VAR

(* === MAIN LOGIC START === *)

(* Safety Interlocks Check *)
IF NOT bEmergencyStop_OK THEN
    bSystemReady := FALSE;
    bCriticalAlarm := TRUE;
    rCO2PumpSpeed_Ref := 0.0;
    rHeaterPower_Ref := 0.0;
    bExtractDischargeValve := FALSE;
    bCascadeValveOpen := FALSE;
    iState := 999; (* Fault State *)
    iOperationState := iState;
    RETURN;
END_IF;

(* Clear faults if safe and disabled *)
IF NOT bEnable AND (iState = 999) THEN
    bCriticalAlarm := FALSE;
    iState := 0;
END_IF;

(* Main State Machine *)
CASE iState OF
    0: (* IDLE & INITIALIZATION *)
        rCO2PumpSpeed_Ref := 0.0;
        rHeaterPower_Ref := 0.0;
        bExtractDischargeValve := FALSE;
        bCascadeValveOpen := FALSE;
        bSystemReady := TRUE;
        
        IF bEnable THEN
            bSystemReady := FALSE;
            tStartupDelay(IN := TRUE, PT := T#2S);
            IF tStartupDelay.Q THEN
                tStartupDelay(IN := FALSE);
                iState := 10; (* PRE-PRESSURIZATION & HEATING *)
            END_IF;
        END_IF;

    10: (* PRE-PRESSURIZATION & HEATING - Bring CO2 to supercritical state *)
        rPressureError := rTargetPressure - rVesselPressure_Bar;
        rTempError := rTargetTemp - rVesselTemp_C;
        
        (* PI Control for Pressure *)
        rPressureIntegral := rPressureIntegral + (rPressureError * Ki_Press);
        IF rPressureIntegral > 100.0 THEN rPressureIntegral := 100.0; END_IF;
        IF rPressureIntegral < 0.0 THEN rPressureIntegral := 0.0; END_IF;
        rCO2PumpSpeed_Ref := (rPressureError * Kp_Press) + rPressureIntegral;
        
        IF rCO2PumpSpeed_Ref > 100.0 THEN rCO2PumpSpeed_Ref := 100.0; END_IF;
        IF rCO2PumpSpeed_Ref < 0.0 THEN rCO2PumpSpeed_Ref := 0.0; END_IF;

        (* PI Control for Temperature *)
        rTempIntegral := rTempIntegral + (rTempError * Ki_Temp);
        IF rTempIntegral > 100.0 THEN rTempIntegral := 100.0; END_IF;
        IF rTempIntegral < 0.0 THEN rTempIntegral := 0.0; END_IF;
        rHeaterPower_Ref := (rTempError * Kp_Temp) + rTempIntegral;
        
        IF rHeaterPower_Ref > 100.0 THEN rHeaterPower_Ref := 100.0; END_IF;
        IF rHeaterPower_Ref < 0.0 THEN rHeaterPower_Ref := 0.0; END_IF;
        
        (* Check if Supercritical condition is reached (Pressure > 73 Bar, Temp > 31.0 C) *)
        IF (rVesselPressure_Bar >= 73.0) AND (rVesselTemp_C >= 31.0) THEN
            iState := 20; (* CONTINUOUS FEED & EXTRACTION *)
        END_IF;
        
        (* Loss of enable *)
        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    20: (* CONTINUOUS FEED & EXTRACTION *)
        (* Maintain Supercritical state *)
        rPressureError := rTargetPressure - rVesselPressure_Bar;
        rCO2PumpSpeed_Ref := (rPressureError * Kp_Press) + 50.0; (* Bias *)
        IF rCO2PumpSpeed_Ref > 100.0 THEN rCO2PumpSpeed_Ref := 100.0; END_IF;
        IF rCO2PumpSpeed_Ref < 0.0 THEN rCO2PumpSpeed_Ref := 0.0; END_IF;

        rTempError := rTargetTemp - rVesselTemp_C;
        rHeaterPower_Ref := (rTempError * Kp_Temp) + 50.0; (* Bias *)
        IF rHeaterPower_Ref > 100.0 THEN rHeaterPower_Ref := 100.0; END_IF;
        IF rHeaterPower_Ref < 0.0 THEN rHeaterPower_Ref := 0.0; END_IF;

        (* Lock Hopper Cascading *)
        IF bLockHopperReady THEN
            bCascadeValveOpen := TRUE;
        ELSE
            bCascadeValveOpen := FALSE;
        END_IF;
        
        (* Cyclonic Separator Extract Recovery *)
        IF rCyclonicSeparatorLevel > 85.0 THEN
            iState := 30; (* DISCHARGE EXTRACT *)
        END_IF;
        
        (* Process deviation alarm *)
        IF (rVesselPressure_Bar < 70.0) OR (rVesselTemp_C < 30.0) THEN
            bCriticalAlarm := TRUE;
            iState := 999;
        END_IF;

        IF NOT bEnable THEN
            bCascadeValveOpen := FALSE;
            iState := 0;
        END_IF;

    30: (* DISCHARGE EXTRACT *)
        bExtractDischargeValve := TRUE;
        tExtractDischargeTimer(IN := TRUE, PT := T#5S);
        
        IF tExtractDischargeTimer.Q OR (rCyclonicSeparatorLevel < 10.0) THEN
            bExtractDischargeValve := FALSE;
            tExtractDischargeTimer(IN := FALSE);
            iState := 20; (* Return to extraction *)
        END_IF;

    999: (* FAULT / SAFE STATE *)
        rCO2PumpSpeed_Ref := 0.0;
        rHeaterPower_Ref := 0.0;
        bExtractDischargeValve := FALSE;
        bCascadeValveOpen := FALSE;
        bSystemReady := FALSE;

END_CASE;

iOperationState := iState;

END_FUNCTION_BLOCK
```"""

import os
os.makedirs("c:/Users/majip/Downloads/LLM REASEARCH/data/swarm_raw", exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"c:/Users/majip/Downloads/LLM REASEARCH/data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
