import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial Scale Lithium Hydroxide (LiOH) Monohydrate Crystallization Reactor**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Spontaneous nucleation boundary supersaturation mapping, draft-tube-baffle (DTB) elutriation leg classification, and exothermic heat of crystallization flash cooling). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_LiOH_Crystallizer\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Scale Lithium Hydroxide (LiOH) Monohydrate Crystallization Reactor

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_LiOH_DTB_Crystallizer
VAR_INPUT
    bEnable                 : BOOL;     (* System master enable signal *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal - active HIGH (Fail-safe) *)
    rFeedConcentration      : REAL;     (* LiOH feed concentration [wt%] *)
    rDraftTubeAgitatorSpeed : REAL;     (* DTB agitator feedback speed [RPM] *)
    rElutriationFlow        : REAL;     (* Fines destruction elutriation flow [m3/h] *)
    rFlashCoolingTemp       : REAL;     (* Flash cooling loop temperature [deg C] *)
    rMotherLiquorLevel      : REAL;     (* Crystallizer vessel level [%] *)
    rSupersaturationRatio   : REAL;     (* Real-time Raman spectroscopy supersaturation index [-] *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* Crystallizer ready for steady-state feed *)
    bWarningSupersaturation : BOOL;     (* Approaching spontaneous nucleation boundary *)
    bAlarm                  : BOOL;     (* Critical fault alarm output *)
    rCoolingWaterValve      : REAL;     (* Control signal to flash cooling condenser CW valve [0-100%] *)
    rElutriationPumpOut     : REAL;     (* Control signal to fines destruction pump [0-100%] *)
    rProductDischargeValve  : REAL;     (* Slurry discharge valve command [0-100%] *)
END_VAR
VAR
    iState                  : INT := 0; 
    tStabilizationTimer     : TON;
    tFaultTimer             : TON;
    rFilteredSupersat       : REAL := 0.0;
    rAlpha                  : REAL := 0.05; (* First-order low pass filter coefficient *)
    bInterlockTriggered     : BOOL := FALSE;
    PID_Cooling             : FB_PID;   (* Conceptual PID for cooling control *)
END_VAR

(* === MAIN LOGIC === *)
(* 1. Multilayered Safety Interlocks *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bAlarm := TRUE;
    rCoolingWaterValve := 100.0; (* Fail-safe full cooling *)
    rElutriationPumpOut := 0.0;
    rProductDischargeValve := 0.0;
    iState := 999; (* FAULT STATE *)
    RETURN;
END_IF;

(* 2. Sensor Noise Filtering - First Order Low Pass on Supersaturation *)
rFilteredSupersat := (rAlpha * rSupersaturationRatio) + ((1.0 - rAlpha) * rFilteredSupersat);

(* 3. Spontaneous Nucleation Boundary Mapping & Alarm *)
IF rFilteredSupersat > 1.15 THEN
    bWarningSupersaturation := TRUE;
ELSE
    bWarningSupersaturation := FALSE;
END_IF;

(* 4. Main State Machine *)
CASE iState OF
    0: (* IDLE & PRE-CHECKS *)
        bSystemReady := FALSE;
        rCoolingWaterValve := 0.0;
        rElutriationPumpOut := 0.0;
        rProductDischargeValve := 0.0;
        bAlarm := FALSE;
        
        IF bEnable AND (rMotherLiquorLevel > 40.0) AND (rDraftTubeAgitatorSpeed > 15.0) THEN
            iState := 10;
        END_IF;

    10: (* INITIAL FLASH COOLING (Exothermic Heat Removal) *)
        rCoolingWaterValve := 50.0; (* Ramp up cooling *)
        tStabilizationTimer(IN := TRUE, PT := T#30S);
        
        IF tStabilizationTimer.Q THEN
            IF rFlashCoolingTemp < 45.0 THEN
                tStabilizationTimer(IN := FALSE);
                iState := 20;
            END_IF;
        END_IF;

    20: (* STEADY STATE CRYSTALLIZATION & ELUTRIATION CONTROL *)
        bSystemReady := TRUE;
        
        (* Cascade control conceptual for cooling based on supersaturation *)
        IF bWarningSupersaturation THEN
            rCoolingWaterValve := MIN(rCoolingWaterValve + 5.0, 100.0);
        ELSE
            rCoolingWaterValve := MAX(rCoolingWaterValve - 1.0, 20.0);
        END_IF;

        (* Elutriation leg classification flow control *)
        IF rElutriationFlow < 5.0 THEN
            rElutriationPumpOut := 60.0;
        ELSIF rElutriationFlow > 15.0 THEN
            rElutriationPumpOut := 30.0;
        END_IF;

        (* Slurry discharge based on level *)
        IF rMotherLiquorLevel > 80.0 THEN
            rProductDischargeValve := 40.0;
        ELSIF rMotherLiquorLevel < 60.0 THEN
            rProductDischargeValve := 0.0;
        END_IF;

        IF NOT bEnable THEN
            iState := 0;
        END_IF;
        
    999: (* FAULT RECOVERY *)
        tFaultTimer(IN := TRUE, PT := T#5S);
        IF bEmergencyStop AND NOT bEnable AND tFaultTimer.Q THEN
            tFaultTimer(IN := FALSE);
            bInterlockTriggered := FALSE;
            bAlarm := FALSE;
            iState := 0;
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

filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
