import json, uuid
import os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Next-Gen Carbon Nanotube (CNT) Forest Chemical Vapor Deposition**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Ethylene/hydrogen precursor mass fraction real-time tuning, floating catalyst (ferrocene) sublimation rate, and 1200°C quartz tube thermal expansion compensation). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_CNT_Forest_CVD\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Next-Gen Carbon Nanotube (CNT) Forest Chemical Vapor Deposition"""

code = """```iec-st
FUNCTION_BLOCK FB_CNT_Forest_CVD_Advanced_Controller
(*
    Title: Next-Generation CNT Forest Chemical Vapor Deposition Controller
    Description: Real-time control of ethylene/hydrogen precursors, ferrocene catalyst sublimation,
                 and dynamic compensation for quartz tube thermal expansion at 1200°C.
    Author: Lumina AI Elite Automation Architect (40-Year Veteran)
*)

VAR_INPUT
    bEnableSys                  : BOOL;   (* System run enable signal, hardware interlocked *)
    bSafetyOK                   : BOOL;   (* Safety relay chain OK, emergency stop circuit *)
    rTempQuartzTube             : REAL;   (* Reactor quartz tube temperature in Celsius [0-1500°C] *)
    rEthyleneMassFlow_Actual    : REAL;   (* Feedback: Ethylene precursor mass flow [sccm] *)
    rHydrogenMassFlow_Actual    : REAL;   (* Feedback: Hydrogen carrier gas mass flow [sccm] *)
    rFerroceneSublimatorTemp    : REAL;   (* Ferrocene sublimator vessel temperature [°C] *)
    rTubePressure_Actual        : REAL;   (* Reactor tube internal pressure [Torr] *)
    rGrowthSubstrateHeight      : REAL;   (* In-situ optical measurement of CNT forest height [um] *)
END_VAR

VAR_OUTPUT
    bSystemReady                : BOOL;   (* Deposition system is stabilized and ready for synthesis *)
    rEthyleneMassFlow_Setpt     : REAL;   (* Commanded Ethylene flow [sccm] *)
    rHydrogenMassFlow_Setpt     : REAL;   (* Commanded Hydrogen flow [sccm] *)
    rFerroceneHeaterPower       : REAL;   (* Power command to sublimation heater [0-100%] *)
    rQuartzHeaterPower          : REAL;   (* Power command to main reactor furnace [0-100%] *)
    bAlarmCritical              : BOOL;   (* Critical process deviation or hardware fault *)
    iCurrentProcessStep         : INT;    (* Active sequence step [0=Idle, 10=Purge, 20=Heat, 30=Deposition, 40=Cool] *)
END_VAR

VAR
    iState                      : INT := 0;
    tStepTimer                  : TON;
    tSafetyDelay                : TON;
    
    (* Internal process variables *)
    rThermalExpansionOffset     : REAL := 0.0;
    rTargetRatioC_H             : REAL := 0.35; (* Optimal Carbon to Hydrogen atomic ratio *)
    rCurrentRatioC_H            : REAL;
    
    (* PID Controllers for Heating (Simplified for ST representation) *)
    rKp_MainFurnace             : REAL := 2.5;
    rKi_MainFurnace             : REAL := 0.015;
    rFurnaceError               : REAL;
    rFurnaceErrorSum            : REAL;
    
    rTargetTempQuartz           : REAL := 1200.0; (* Standard CNT growth temperature *)
    rMaxTempDev                 : REAL := 5.0;    (* Max allowed temperature deviation *)
END_VAR

(* === SAFETY & INTERLOCKS === *)
IF NOT bSafetyOK THEN
    bSystemReady := FALSE;
    bAlarmCritical := TRUE;
    iState := 999; (* Fault state *)
    rEthyleneMassFlow_Setpt := 0.0;
    rHydrogenMassFlow_Setpt := 100.0; (* Safe purge flow *)
    rFerroceneHeaterPower := 0.0;
    rQuartzHeaterPower := 0.0;
    iCurrentProcessStep := iState;
    RETURN;
END_IF;

IF NOT bEnableSys AND iState <> 999 THEN
    iState := 0;
END_IF;

(* === MAIN PROCESS STATE MACHINE === *)
CASE iState OF
    0: (* IDLE *)
        bSystemReady := FALSE;
        bAlarmCritical := FALSE;
        rEthyleneMassFlow_Setpt := 0.0;
        rHydrogenMassFlow_Setpt := 0.0;
        rQuartzHeaterPower := 0.0;
        rFerroceneHeaterPower := 0.0;
        
        IF bEnableSys THEN
            iState := 10;
        END_IF;

    10: (* PURGE REACTOR TUBE *)
        (* Flow H2 at high rate to clear O2 and moisture *)
        rHydrogenMassFlow_Setpt := 1000.0; 
        rEthyleneMassFlow_Setpt := 0.0;
        
        tStepTimer(IN := TRUE, PT := T#300S);
        IF tStepTimer.Q THEN
            tStepTimer(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* HEATING & THERMAL EXPANSION COMPENSATION *)
        (* Ramp reactor to 1200C. Model quartz thermal expansion: alpha = 5.5e-7 /K *)
        rFurnaceError := rTargetTempQuartz - rTempQuartzTube;
        rFurnaceErrorSum := rFurnaceErrorSum + rFurnaceError;
        
        (* PI Control calculation for Main Furnace *)
        rQuartzHeaterPower := (rFurnaceError * rKp_MainFurnace) + (rFurnaceErrorSum * rKi_MainFurnace);
        IF rQuartzHeaterPower > 100.0 THEN rQuartzHeaterPower := 100.0; END_IF;
        IF rQuartzHeaterPower < 0.0 THEN rQuartzHeaterPower := 0.0; END_IF;
        
        (* Calculate geometric deformation of the quartz tube due to thermal expansion at 1200C *)
        rThermalExpansionOffset := rTempQuartzTube * 0.00000055 * 1000.0; (* Simplified linear strain offset *)
        
        (* Warm up Ferrocene sublimator to 90C *)
        IF rFerroceneSublimatorTemp < 90.0 THEN
            rFerroceneHeaterPower := 35.0;
        ELSE
            rFerroceneHeaterPower := 15.0; (* Maintain *)
        END_IF;
        
        IF ABS(rFurnaceError) < rMaxTempDev AND rFerroceneSublimatorTemp >= 90.0 THEN
            tStepTimer(IN := TRUE, PT := T#600S); (* Thermal stabilization soak *)
            IF tStepTimer.Q THEN
                tStepTimer(IN := FALSE);
                bSystemReady := TRUE;
                iState := 30;
            END_IF;
        ELSE
            tStepTimer(IN := FALSE);
        END_IF;

    30: (* CNT FOREST GROWTH (CVD) *)
        (* Calculate dynamic C:H ratio to maintain optimal precursor cracking physics *)
        IF rHydrogenMassFlow_Actual > 0.0 THEN
            rCurrentRatioC_H := rEthyleneMassFlow_Actual / rHydrogenMassFlow_Actual;
        ELSE
            rCurrentRatioC_H := 0.0;
        END_IF;
        
        (* Introduce Ethylene precursor *)
        rHydrogenMassFlow_Setpt := 500.0;
        rEthyleneMassFlow_Setpt := 500.0 * rTargetRatioC_H;
        
        (* Monitor growth height. Stop at 500 microns *)
        IF rGrowthSubstrateHeight >= 500.0 THEN
            iState := 40;
        END_IF;
        
        (* Pressure interlock during growth phase *)
        IF rTubePressure_Actual > 15.0 THEN (* Exceeds nominal 10 Torr base by 50% *)
            bAlarmCritical := TRUE;
            iState := 999;
        END_IF;

    40: (* COOLING & ANNEALING *)
        bSystemReady := FALSE;
        rEthyleneMassFlow_Setpt := 0.0;
        rQuartzHeaterPower := 0.0;
        rFerroceneHeaterPower := 0.0;
        
        (* Cool under H2 flow to prevent oxidation of the fresh CNTs *)
        rHydrogenMassFlow_Setpt := 200.0;
        
        IF rTempQuartzTube < 100.0 THEN
            iState := 0; (* Cycle complete, return to idle *)
        END_IF;
        
    999: (* FAULT HANDLING *)
        (* Abort safely: shut off precursors and heat, flush with H2 *)
        rEthyleneMassFlow_Setpt := 0.0;
        rHydrogenMassFlow_Setpt := 500.0;
        rQuartzHeaterPower := 0.0;
        rFerroceneHeaterPower := 0.0;
        
        IF bSafetyOK AND NOT bEnableSys THEN
            bAlarmCritical := FALSE;
            iState := 0; (* Reset fault when enable is dropped *)
        END_IF;

END_CASE;

iCurrentProcessStep := iState;

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
