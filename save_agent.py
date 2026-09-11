import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Deep-Space Atmospheric Entry Aeroshell Ablation Monitor**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., High-enthalpy plasma sheath RF attenuation tracking, phenolics pyrolysis endothermic reaction mapping, and multi-depth char-layer thermocouple regression). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_AeroshellAblationMonitor\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Deep-Space Atmospheric Entry Aeroshell Ablation Monitor

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.
</USER_REQUEST>"""

code = """```iec-st
FUNCTION_BLOCK FB_AeroshellAblationMonitor
(*
    =============================================================================
    Deep-Space Atmospheric Entry Aeroshell Ablation Monitor
    Domain: Aerospace Control Systems / Re-entry Vehicle Health Management
    Description:
      Monitors high-enthalpy plasma sheath RF attenuation, mapping of phenolics
      pyrolysis endothermic reactions, and multi-depth char-layer thermocouple
      regression to estimate aeroshell integrity during atmospheric entry.
    =============================================================================
*)
VAR_INPUT
    bEnable                 : BOOL;     (* System enable signal / Entry phase armed *)
    bEmergencyStop          : BOOL;     (* Safety interlock / Vehicle safe mode active *)
    rHeatShieldTempSurface  : REAL;     (* Surface temperature from pyrometer [K] *)
    rHeatShieldTempDepth1   : REAL;     (* Embedded TC at depth 1 (2mm) [K] *)
    rHeatShieldTempDepth2   : REAL;     (* Embedded TC at depth 2 (5mm) [K] *)
    rHeatShieldTempDepth3   : REAL;     (* Embedded TC at depth 3 (10mm) [K] *)
    rRFAttenuation          : REAL;     (* Plasma sheath RF attenuation [dB] *)
    rDynamicPressure        : REAL;     (* Freestream dynamic pressure [Pa] *)
END_VAR

VAR_OUTPUT
    bSystemReady            : BOOL;     (* Monitor initialized and ready *)
    rAblationRate           : REAL;     (* Estimated surface recession rate [mm/s] *)
    rCharLayerThickness     : REAL;     (* Estimated char layer thickness [mm] *)
    bThermalWarning         : BOOL;     (* Non-nominal thermal profile detected *)
    bStructuralFailureRisk  : BOOL;     (* High probability of burn-through / failure *)
    iState                  : INT;      (* Current monitor state *)
END_VAR

VAR
    iInternalState          : INT := 0; 
    tUpdateTimer            : TON;
    rFilteredSurfaceTemp    : REAL := 0.0;
    rPrevSurfaceTemp        : REAL := 0.0;
    rTempDerivative         : REAL := 0.0;
    
    (* Arrays for thermal gradient mapping *)
    aTempProfile            : ARRAY[1..4] OF REAL;
    
    (* Constants for phenolics ablation model *)
    c_rPyrolysisTempStart   : REAL := 600.0;  (* [K] *)
    c_rPyrolysisTempEnd     : REAL := 950.0;  (* [K] *)
    c_rAlpha                : REAL := 0.85;   (* Low-pass filter coefficient *)
    
    bPlasmaBlackoutActive   : BOOL := FALSE;
END_VAR

(* === MAIN LOGIC === *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bThermalWarning := TRUE;
    bStructuralFailureRisk := TRUE;
    rAblationRate := 0.0;
    rCharLayerThickness := 0.0;
    iState := -1;
    RETURN;
END_IF;

(* Filter noisy pyrometer surface readings *)
rFilteredSurfaceTemp := (c_rAlpha * rFilteredSurfaceTemp) + ((1.0 - c_rAlpha) * rHeatShieldTempSurface);
rTempDerivative := (rFilteredSurfaceTemp - rPrevSurfaceTemp) / 0.1; (* Assuming 100ms cycle *)
rPrevSurfaceTemp := rFilteredSurfaceTemp;

(* Assign arrays for easier processing *)
aTempProfile[1] := rFilteredSurfaceTemp;
aTempProfile[2] := rHeatShieldTempDepth1;
aTempProfile[3] := rHeatShieldTempDepth2;
aTempProfile[4] := rHeatShieldTempDepth3;

CASE iInternalState OF
    0: (* IDLE & INITIALIZATION *)
        rAblationRate := 0.0;
        rCharLayerThickness := 0.0;
        bThermalWarning := FALSE;
        bStructuralFailureRisk := FALSE;
        IF bEnable THEN
            bSystemReady := TRUE;
            iInternalState := 10;
        END_IF;
        
    10: (* MONITORING ATMOSPHERIC ENTRY *)
        (* Check plasma blackout conditions *)
        IF rRFAttenuation > 45.0 AND rDynamicPressure > 1000.0 THEN
            bPlasmaBlackoutActive := TRUE;
        ELSE
            bPlasmaBlackoutActive := FALSE;
        END_IF;
        
        (* Estimate char layer thickness based on pyrolysis isotherm tracking *)
        IF aTempProfile[4] > c_rPyrolysisTempStart THEN
            rCharLayerThickness := 10.0;
        ELSIF aTempProfile[3] > c_rPyrolysisTempStart THEN
            rCharLayerThickness := 5.0 + 5.0 * ((aTempProfile[3] - c_rPyrolysisTempStart) / (c_rPyrolysisTempEnd - c_rPyrolysisTempStart));
        ELSIF aTempProfile[2] > c_rPyrolysisTempStart THEN
            rCharLayerThickness := 2.0 + 3.0 * ((aTempProfile[2] - c_rPyrolysisTempStart) / (c_rPyrolysisTempEnd - c_rPyrolysisTempStart));
        ELSE
            rCharLayerThickness := 0.0;
        END_IF;
        
        (* Estimate instantaneous ablation rate via surface temperature derivative and dynamic pressure *)
        IF rFilteredSurfaceTemp > 1800.0 THEN
            rAblationRate := (rFilteredSurfaceTemp - 1800.0) * 0.005 + (rDynamicPressure * 0.0001);
        ELSE
            rAblationRate := 0.0;
        END_IF;
        
        (* Evaluate Safety Constraints *)
        IF rCharLayerThickness > 8.0 AND rAblationRate > 0.5 THEN
            bThermalWarning := TRUE;
        END_IF;
        
        IF (rAblationRate > 1.5) OR (aTempProfile[4] > 800.0 AND rDynamicPressure > 50000.0) THEN
            bStructuralFailureRisk := TRUE;
        END_IF;
        
        IF NOT bEnable THEN
            iInternalState := 0;
            bSystemReady := FALSE;
        END_IF;
        
    ELSE
        (* FAULT STATE *)
        bThermalWarning := TRUE;
        bStructuralFailureRisk := TRUE;
        IF NOT bEnable THEN
            iInternalState := 0;
        END_IF;
        
END_CASE;

iState := iInternalState;

END_FUNCTION_BLOCK
```"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}

filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
