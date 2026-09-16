import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Commercial HVAC Chilled Water Plant Multi-Compressor Sequencing and Load Shedding**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_ChillerPlant_Sequencing\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Commercial HVAC Chilled Water Plant Multi-Compressor Sequencing and Load Shedding

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_ChilledWaterPlant_LoadShedding
VAR_INPUT
    (* Main plant control and safety *)
    bPlantEnable            : BOOL;     (* Main enable command for the plant *)
    bEmergencyStop          : BOOL;     (* Safety relay OK / emergency stop circuit *)
    bFireAlarmInterlock     : BOOL;     (* Fire alarm system interlock (normally closed) *)
    
    (* Physical measurements *)
    rChW_SupplyTemp         : REAL;     (* Chilled water supply temperature (deg C) *)
    rChW_ReturnTemp         : REAL;     (* Chilled water return temperature (deg C) *)
    rPlantFlowRate          : REAL;     (* Total plant chilled water flow rate (L/s) *)
    rTotalElectricalLoad    : REAL;     (* Facility total electrical load (kW) *)
    rMaxAllowedLoad         : REAL;     (* Maximum allowed load before shedding (kW) *)
    
    (* Chiller statuses *)
    bChiller1_Available     : BOOL;     (* Chiller 1 no fault and available *)
    bChiller2_Available     : BOOL;     (* Chiller 2 no fault and available *)
    bChiller3_Available     : BOOL;     (* Chiller 3 no fault and available *)
    bChiller4_Available     : BOOL;     (* Chiller 4 no fault and available *)
END_VAR

VAR_OUTPUT
    (* Plant outputs *)
    bPlantRunning           : BOOL;     (* Plant is active and in normal operation *)
    bAlarmCriticalFault     : BOOL;     (* Critical fault requiring immediate attention *)
    bLoadSheddingActive     : BOOL;     (* Indication that plant capacity is being curtailed *)
    
    (* Chiller commands *)
    rChiller1_CmdLoad       : REAL;     (* Chiller 1 load command 0-100% *)
    rChiller2_CmdLoad       : REAL;     (* Chiller 2 load command 0-100% *)
    rChiller3_CmdLoad       : REAL;     (* Chiller 3 load command 0-100% *)
    rChiller4_CmdLoad       : REAL;     (* Chiller 4 load command 0-100% *)
END_VAR

VAR
    (* Internal State *)
    iSeqState               : INT := 0; (* Main sequence state machine *)
    iActiveChillers         : INT := 0; (* Number of chillers currently requested *)
    
    (* Control Variables *)
    rSetpoint               : REAL := 6.5;  (* Default chilled water setpoint (deg C) *)
    rTempError              : REAL;
    rIntegralTerm           : REAL := 0.0;
    rCoolingDemand          : REAL;     (* Normalized demand 0-400% *)
    rFilteredSupplyTemp     : REAL;
    
    (* PID Parameters *)
    rKp                     : REAL := 3.5;
    rKi                     : REAL := 0.12;
    
    (* Timers *)
    tControlTimer           : TON;
    tStageDelay             : TON;
    
    (* Load Shedding Variables *)
    bShedStage1             : BOOL := FALSE;
    bShedStage2             : BOOL := FALSE;
END_VAR

(* === MAIN SAFETY INTERLOCKS === *)
IF NOT bEmergencyStop OR NOT bFireAlarmInterlock THEN
    bPlantRunning := FALSE;
    bAlarmCriticalFault := TRUE;
    rChiller1_CmdLoad := 0.0;
    rChiller2_CmdLoad := 0.0;
    rChiller3_CmdLoad := 0.0;
    rChiller4_CmdLoad := 0.0;
    bLoadSheddingActive := FALSE;
    iSeqState := 0;
    RETURN;
END_IF;

bAlarmCriticalFault := FALSE;

(* === SENSOR NOISE FILTERING === *)
(* Exponential Moving Average filter for supply temperature (Alpha = 0.1) *)
IF rFilteredSupplyTemp < 1.0 OR rFilteredSupplyTemp > 30.0 THEN
    rFilteredSupplyTemp := rChW_SupplyTemp; (* Initialize if out of bounds *)
ELSE
    rFilteredSupplyTemp := (rFilteredSupplyTemp * 0.9) + (rChW_SupplyTemp * 0.1);
END_IF;

(* === LOAD SHEDDING LOGIC === *)
(* Staged load shedding based on total electrical demand vs maximum allowed *)
IF rTotalElectricalLoad > (rMaxAllowedLoad * 0.98) THEN
    bShedStage2 := TRUE;
    bShedStage1 := TRUE;
    bLoadSheddingActive := TRUE;
ELSIF rTotalElectricalLoad > (rMaxAllowedLoad * 0.90) THEN
    bShedStage2 := FALSE;
    bShedStage1 := TRUE;
    bLoadSheddingActive := TRUE;
ELSE
    bShedStage2 := FALSE;
    bShedStage1 := FALSE;
    bLoadSheddingActive := FALSE;
END_IF;

(* === MAIN CONTROL SEQUENCE === *)
CASE iSeqState OF
    0: (* IDLE *)
        bPlantRunning := FALSE;
        rChiller1_CmdLoad := 0.0;
        rChiller2_CmdLoad := 0.0;
        rChiller3_CmdLoad := 0.0;
        rChiller4_CmdLoad := 0.0;
        iActiveChillers := 0;
        
        IF bPlantEnable THEN
            iSeqState := 10;
        END_IF;

    10: (* PID CALCULATION & DEMAND ASSESSMENT *)
        bPlantRunning := TRUE;
        tControlTimer(IN := TRUE, PT := T#2S);
        
        IF tControlTimer.Q THEN
            tControlTimer(IN := FALSE);
            
            (* Calculate Control Error *)
            rTempError := rFilteredSupplyTemp - rSetpoint;
            
            (* Anti-windup Integral Calculation *)
            rIntegralTerm := rIntegralTerm + (rTempError * rKi);
            IF rIntegralTerm > 400.0 THEN rIntegralTerm := 400.0; END_IF;
            IF rIntegralTerm < 0.0 THEN rIntegralTerm := 0.0; END_IF;
            
            (* Total Cooling Demand (0% to 400% representing up to 4 chillers) *)
            rCoolingDemand := (rTempError * rKp) + rIntegralTerm;
            IF rCoolingDemand < 0.0 THEN rCoolingDemand := 0.0; END_IF;
            IF rCoolingDemand > 400.0 THEN rCoolingDemand := 400.0; END_IF;
            
            (* Chiller Staging Logic based on demand *)
            IF rCoolingDemand > 310.0 AND bChiller4_Available THEN
                iActiveChillers := 4;
            ELSIF rCoolingDemand > 210.0 AND bChiller3_Available THEN
                iActiveChillers := 3;
            ELSIF rCoolingDemand > 110.0 AND bChiller2_Available THEN
                iActiveChillers := 2;
            ELSIF rCoolingDemand > 10.0 AND bChiller1_Available THEN
                iActiveChillers := 1;
            ELSE
                iActiveChillers := 0;
            END_IF;
            
            (* Apply Load Shedding Curtailment *)
            IF bShedStage2 AND iActiveChillers > 1 THEN
                (* Extreme load shedding: limit to 1 chiller *)
                iActiveChillers := 1;
            ELSIF bShedStage1 AND iActiveChillers > 2 THEN
                (* Moderate load shedding: limit to 2 chillers maximum *)
                iActiveChillers := 2;
            END_IF;
            
            iSeqState := 20;
        END_IF;
        
        IF NOT bPlantEnable THEN
            iSeqState := 0;
        END_IF;

    20: (* STAGING DELAY ENFORCEMENT *)
        tStageDelay(IN := TRUE, PT := T#45S);
        
        IF tStageDelay.Q OR iActiveChillers = 0 THEN
            tStageDelay(IN := FALSE);
            iSeqState := 30;
        END_IF;

    30: (* COMMAND DISPATCHING *)
        (* Reset commands *)
        rChiller1_CmdLoad := 0.0;
        rChiller2_CmdLoad := 0.0;
        rChiller3_CmdLoad := 0.0;
        rChiller4_CmdLoad := 0.0;
        
        IF iActiveChillers > 0 THEN
            (* Distribute normalized load evenly across active chillers *)
            rChiller1_CmdLoad := rCoolingDemand / INT_TO_REAL(iActiveChillers);
            
            IF iActiveChillers >= 2 THEN rChiller2_CmdLoad := rChiller1_CmdLoad; END_IF;
            IF iActiveChillers >= 3 THEN rChiller3_CmdLoad := rChiller1_CmdLoad; END_IF;
            IF iActiveChillers >= 4 THEN rChiller4_CmdLoad := rChiller1_CmdLoad; END_IF;
        END_IF;
        
        (* Enforce per-chiller max limits (100% capacity) *)
        IF rChiller1_CmdLoad > 100.0 THEN rChiller1_CmdLoad := 100.0; END_IF;
        IF rChiller2_CmdLoad > 100.0 THEN rChiller2_CmdLoad := 100.0; END_IF;
        IF rChiller3_CmdLoad > 100.0 THEN rChiller3_CmdLoad := 100.0; END_IF;
        IF rChiller4_CmdLoad > 100.0 THEN rChiller4_CmdLoad := 100.0; END_IF;
        
        iSeqState := 10; (* Return to PID loop *)

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
