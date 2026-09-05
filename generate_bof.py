import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Automated Steel Mill Basic Oxygen Furnace (BOF) Oxygen Lance**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., supersonic oxygen flow rate decarb profiling, dynamic lance height acoustic mapping for slag foaming, and off-gas CO/CO2 ratio feed-forward logic). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_BOF_OxygenLance\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Automated Steel Mill Basic Oxygen Furnace (BOF) Oxygen Lance

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_BOF_OxygenLanceControl
VAR_INPUT
    (* System Interlocks *)
    bEnable             : BOOL;     (* Main sequence enable signal *)
    bEmergencyStop      : BOOL;     (* Safety relay OK signal, normally high *)
    (* Process Measurements *)
    rAcousticIntensity  : REAL;     (* Acoustic sensor reading [dB] for slag foam index *)
    rOffGasCO           : REAL;     (* Off-gas Carbon Monoxide concentration [%] *)
    rOffGasCO2          : REAL;     (* Off-gas Carbon Dioxide concentration [%] *)
    rBathTemp           : REAL;     (* Pyrometer/Sublance bath temperature [degC] *)
    rLanceHeightAct     : REAL;     (* Actual lance height above nominal bath level [m] *)
    rTotalO2Blown       : REAL;     (* Accumulated Oxygen blown [Nm3] *)
END_VAR
VAR_OUTPUT
    (* Actuator Commands and Status *)
    bSystemReady        : BOOL;     (* Ready to begin blow sequence *)
    rOxygenFlowSetpt    : REAL;     (* Supersonic oxygen flow rate setpoint [Nm3/min] *)
    rLanceHeightSetpt   : REAL;     (* Target lance hoist height [m] *)
    bSlagFoamAlarm      : BOOL;     (* Slopping or dry slag hazard alarm *)
    bBlowComplete       : BOOL;     (* End of blow milestone reached *)
    iPhaseSequence      : INT;      (* Current active phase ID *)
END_VAR
VAR
    (* Internal State & Timers *)
    iState              : INT := 0; 
    tPhaseTimer         : TON;
    rDecarbRate         : REAL;
    rPostCombRatio      : REAL;
    
    (* Tuning Parameters & Constants *)
    MAX_LANCE_HEIGHT    : REAL := 3.5;
    MIN_LANCE_HEIGHT    : REAL := 1.2;
    MAX_O2_FLOW         : REAL := 1200.0;
    IGNITION_O2         : REAL := 600.0;
    DESIRED_ACOUSTIC    : REAL := 45.0; (* dB target for optimal foaming *)
END_VAR

(* === MAIN SAFETY AND INTERLOCK LOGIC === *)
IF NOT bEmergencyStop THEN
    bSystemReady      := FALSE;
    rOxygenFlowSetpt  := 0.0;
    rLanceHeightSetpt := MAX_LANCE_HEIGHT;
    bSlagFoamAlarm    := TRUE;
    iState            := 999; (* Fault state *)
    RETURN;
END_IF;

(* === PROCESS CALCULATIONS === *)
(* Calculate Post-Combustion Ratio (PCR) from Off-Gas analysis *)
IF (rOffGasCO + rOffGasCO2) > 0.001 THEN
    rPostCombRatio := rOffGasCO2 / (rOffGasCO + rOffGasCO2);
ELSE
    rPostCombRatio := 0.0;
END_IF;

(* Estimated Decarburization Rate (dC/dt) proportional to total carbon gas evolution *)
rDecarbRate := (rOffGasCO + rOffGasCO2) * rTotalO2Blown * 0.0053; 

(* === DYNAMIC PHASE CONTROL SEQUENCE === *)
CASE iState OF
    0: (* IDLE & INITIALIZATION *)
        bSystemReady      := TRUE;
        bBlowComplete     := FALSE;
        rOxygenFlowSetpt  := 0.0;
        rLanceHeightSetpt := MAX_LANCE_HEIGHT;
        
        IF bEnable THEN
            iState := 10; (* Transition to Ignition *)
        END_IF;

    10: (* IGNITION PHASE *)
        iPhaseSequence    := 1;
        rLanceHeightSetpt := 2.5;  (* High lance for ignition *)
        rOxygenFlowSetpt  := IGNITION_O2;
        
        tPhaseTimer(IN := TRUE, PT := T#45S);
        IF tPhaseTimer.Q THEN
            tPhaseTimer(IN := FALSE);
            iState := 20; (* Main Blow Phase *)
        END_IF;

    20: (* MAIN BLOW - DYNAMIC SLAG FOAMING CONTROL *)
        iPhaseSequence    := 2;
        rOxygenFlowSetpt  := MAX_O2_FLOW;
        
        (* Closed-loop lance height control using acoustic mapping for slag foaming *)
        IF rAcousticIntensity > (DESIRED_ACOUSTIC + 5.0) THEN
            (* Slag is too dry, acoustic noise is high, lower lance to increase FeO generation *)
            rLanceHeightSetpt := LIMIT(MIN_LANCE_HEIGHT, rLanceHeightAct - 0.1, MAX_LANCE_HEIGHT);
        ELSIF rAcousticIntensity < (DESIRED_ACOUSTIC - 5.0) THEN
            (* Slag is overly foamy (slopping risk), acoustic is muffled, raise lance *)
            rLanceHeightSetpt := LIMIT(MIN_LANCE_HEIGHT, rLanceHeightAct + 0.1, MAX_LANCE_HEIGHT);
        END_IF;
        
        (* Transition based on accumulated oxygen or early temperature measurement *)
        IF rTotalO2Blown > 15000.0 THEN
            iState := 30;
        END_IF;

    30: (* DECARBURIZATION PROFILING PHASE *)
        iPhaseSequence    := 3;
        rLanceHeightSetpt := 1.5; (* Hard blow for mixing and rapid decarburization *)
        
        (* Feed-forward control: reduce O2 flow as decarb rate begins to drop (catch-carbon) *)
        IF rDecarbRate < 0.15 AND rPostCombRatio > 0.4 THEN
            rOxygenFlowSetpt := MAX_O2_FLOW * 0.75;
            iState := 40;
        ELSE
            rOxygenFlowSetpt := MAX_O2_FLOW;
        END_IF;

    40: (* END BLOW CATCH-CARBON *)
        iPhaseSequence    := 4;
        
        (* Final trimming based on bath temperature trajectory *)
        IF rBathTemp >= 1650.0 OR NOT bEnable THEN
            iState := 50;
        END_IF;

    50: (* SEQUENCE COMPLETE *)
        iPhaseSequence    := 5;
        bBlowComplete     := TRUE;
        rOxygenFlowSetpt  := 0.0;
        rLanceHeightSetpt := MAX_LANCE_HEIGHT;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    999: (* FAULT HANDLING *)
        iPhaseSequence    := 99;
        rOxygenFlowSetpt  := 0.0;
        rLanceHeightSetpt := MAX_LANCE_HEIGHT;
        IF bEmergencyStop AND NOT bEnable THEN
            iState := 0;
        END_IF;
END_CASE;

(* Slag slopping alarm generation *)
bSlagFoamAlarm := (rAcousticIntensity < 15.0 AND iState = 20);

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
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
