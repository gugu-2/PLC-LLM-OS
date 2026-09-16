import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Next-Generation Spacecraft Closed-Loop Life Support System (ECLSS)**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Sabatier reaction methanation control, trace contaminant adsorption bed sequencing, and zero-G hydroponic water recovery). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_ECLSS_LifeSupport\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Next-Generation Spacecraft Closed-Loop Life Support System (ECLSS)

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_ECLSS_SabatierReactor_Control
VAR_INPUT
    (* Required: at least 4-8 physical inputs with types and comments *)
    bEnable         : BOOL;     (* System enable signal for the Sabatier Methanation process *)
    bEmergencyStop  : BOOL;     (* Safety relay OK signal; FALSE means Emergency Stop Active *)
    rCO2_FlowRate   : REAL;     (* Physical measurement: Carbon Dioxide inflow rate (kg/hr) *)
    rH2_FlowRate    : REAL;     (* Physical measurement: Hydrogen gas inflow rate (kg/hr) *)
    rReactorTemp    : REAL;     (* Physical measurement: Sabatier reactor core temperature in deg C *)
    rReactorPress   : REAL;     (* Physical measurement: Sabatier reactor pressure in kPa *)
    rMethaneConc    : REAL;     (* Physical measurement: Outflow methane concentration (%) *)
END_VAR
VAR_OUTPUT
    (* Required: at least 3-6 outputs with types and comments *)
    bSystemReady    : BOOL;     (* System ready status; TRUE when Sabatier reaction is optimal *)
    rHeaterControl  : REAL;     (* Control signal to reactor pre-heater (0.0 to 100.0%) *)
    rCoolingValve   : REAL;     (* Control signal to thermal cooling loop valve (0.0 to 100.0%) *)
    bVentValve      : BOOL;     (* Sabatier product off-gas vent valve state *)
    bAlarm          : BOOL;     (* Fault alarm output (High temp/press/ratio error) *)
END_VAR
VAR
    (* Internal state variables *)
    iState          : INT := 0;
    tTimer          : TON;
    tWarmupTimer    : TON;
    
    (* PID and Filtering Variables *)
    rFilteredTemp   : REAL := 20.0;
    rTempAlpha      : REAL := 0.05; (* Low pass filter coefficient *)
    rTargetTemp     : REAL := 420.0; (* Optimal Sabatier exothermic temp *)
    
    rH2_CO2_Ratio   : REAL := 0.0;
    rOptimalRatio   : REAL := 4.0;  (* Stoichiometric ratio: 4 H2 to 1 CO2 *)
    
    (* Error tracking *)
    iFaultCode      : INT := 0;
END_VAR

(* === MAIN LOGIC === *)
(* Filter physical sensor inputs to remove noise in zero-G environment *)
rFilteredTemp := (rTempAlpha * rReactorTemp) + ((1.0 - rTempAlpha) * rFilteredTemp);

(* 
 * Critical Safety Interlock - Multi-layered Protection
 * Ensures sabatier reactor does not exceed explosive limits 
 *)
IF NOT bEmergencyStop OR (rReactorPress > 2000.0) OR (rFilteredTemp > 650.0) THEN
    bSystemReady := FALSE;
    rHeaterControl := 0.0;
    rCoolingValve := 100.0; (* Maximum cooling during emergency *)
    bVentValve := TRUE;     (* Depressurize the reactor *)
    bAlarm := TRUE;
    iFaultCode := 9999;     (* Critical hardware or interlock fault *)
    iState := 99;           (* Force to FAULT state *)
    RETURN;
END_IF;

(* Main Sabatier Methanation State Machine *)
CASE iState OF
    0: (* IDLE *)
        bSystemReady := FALSE;
        rHeaterControl := 0.0;
        rCoolingValve := 0.0;
        bVentValve := FALSE;
        bAlarm := FALSE;
        iFaultCode := 0;
        
        IF bEnable THEN
            iState := 10;
        END_IF;

    10: (* PREHEAT PHASE *)
        (* Bring the Sabatier reactor up to ignition temperature (approx 300C) *)
        IF rFilteredTemp < 300.0 THEN
            rHeaterControl := 80.0; (* 80% heater power *)
            rCoolingValve := 0.0;
        ELSE
            rHeaterControl := 20.0; (* Maintenance heat *)
            tWarmupTimer(IN := TRUE, PT := T#10S);
            IF tWarmupTimer.Q THEN
                tWarmupTimer(IN := FALSE);
                iState := 20;
            END_IF;
        END_IF;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    20: (* RUNNING & EXOTHERMIC REGULATION *)
        bSystemReady := TRUE;
        
        (* Calculate Sabatier Flow Ratio (Safe H2/CO2 stoichiometry) *)
        IF rCO2_FlowRate > 0.0 THEN
            rH2_CO2_Ratio := rH2_FlowRate / rCO2_FlowRate;
        ELSE
            rH2_CO2_Ratio := 0.0;
        END_IF;

        (* Exothermic Heat Management *)
        IF rFilteredTemp > rTargetTemp THEN
            (* Sabatier is highly exothermic; increase cooling loop proportionally *)
            rCoolingValve := 10.0 + ((rFilteredTemp - rTargetTemp) * 2.5);
            IF rCoolingValve > 100.0 THEN 
                rCoolingValve := 100.0; 
            END_IF;
            rHeaterControl := 0.0;
        ELSE
            (* Reaction is cooling down too much, apply maintenance heat *)
            rCoolingValve := 0.0;
            rHeaterControl := 10.0 + ((rTargetTemp - rFilteredTemp) * 1.5);
            IF rHeaterControl > 100.0 THEN 
                rHeaterControl := 100.0; 
            END_IF;
        END_IF;

        (* Quality Control on Methane Output *)
        IF rMethaneConc < 85.0 THEN
            bVentValve := TRUE; (* Dump sub-par mixture to trace contaminant bed *)
        ELSE
            bVentValve := FALSE; (* Route pure CH4 to storage or exhaust *)
        END_IF;
        
        (* Fault Detection: Improper Stoichiometry *)
        IF rH2_CO2_Ratio < 3.5 OR rH2_CO2_Ratio > 4.5 THEN
            tTimer(IN := TRUE, PT := T#30S);
            IF tTimer.Q THEN
                bAlarm := TRUE;
                iFaultCode := 101; (* Mix ratio fault *)
                iState := 40;
            END_IF;
        ELSE
            tTimer(IN := FALSE);
        END_IF;

        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    40: (* NON-CRITICAL FAULT *)
        bSystemReady := FALSE;
        rHeaterControl := 0.0;
        rCoolingValve := 50.0; (* Safe cooling *)
        bVentValve := TRUE;    (* Vent anomalous mixture *)
        
        (* Await reset (bEnable cycled) *)
        IF NOT bEnable THEN
            bAlarm := FALSE;
            iState := 0;
        END_IF;
        
    99: (* CRITICAL INTERLOCK FAULT LATCH *)
        (* Handled globally at start of block. Await power cycle or hard reset *)
        ;

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
