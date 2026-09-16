import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Supercritical Water Oxidation (SCWO) Hazardous Waste Destruction**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Extreme temperature/pressure letdown valve staging, exothermic reaction thermal runaway prevention, and corrosive salt precipitation scraping). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_SCWO_WasteDestruction\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Supercritical Water Oxidation (SCWO) Hazardous Waste Destruction

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_SCWO_WasteDestruction
(*========================================================================
   FUNCTION BLOCK: FB_SCWO_WasteDestruction
   DOMAIN: Supercritical Water Oxidation (SCWO) Hazardous Waste Destruction
   DESCRIPTION:
   Manages the exothermic oxidation of hazardous waste in a supercritical 
   water reactor (>374 deg C, >22.1 MPa). Implements cascaded pressure 
   letdown control, rapid thermal quench logic for thermal runaway 
   prevention, and continuous salt scraper management to prevent fouling.
   =========================================================================*)
VAR_INPUT
    bSystemEnable       : BOOL;     (* System master enable signal *)
    bEmergencyStop      : BOOL;     (* Safety relay loop OK signal, active high *)
    rReactorTemp_C      : REAL;     (* Reactor core temperature [Celsius] *)
    rReactorPress_MPa   : REAL;     (* Reactor internal pressure [MPa] *)
    rOxidantFlow_kg_h   : REAL;     (* Oxidant feed mass flow rate [kg/h] *)
    rWasteFlow_kg_h     : REAL;     (* Waste feed mass flow rate [kg/h] *)
    rEffluentpH         : REAL;     (* Effluent pH measurement for corrosion prep *)
    rCoolingWater_C     : REAL;     (* Cooling water inlet temperature [Celsius] *)
END_VAR

VAR_OUTPUT
    bSystemReady        : BOOL;     (* System is ready for waste injection *)
    rLetdownValve1_Pos  : REAL;     (* Primary pressure letdown valve position 0-100% *)
    rLetdownValve2_Pos  : REAL;     (* Secondary pressure letdown valve position 0-100% *)
    bQuenchActivate     : BOOL;     (* Rapid thermal quench system trigger *)
    bScraperMotorRun    : BOOL;     (* Salt scraper motor contactor command *)
    bCriticalAlarm      : BOOL;     (* Critical fault alarm, interlock triggered *)
    rHeaterCmd_kW       : REAL;     (* Pre-heater command [kW] *)
END_VAR

VAR
    (* Internal State Variables *)
    iScwoState          : INT := 0; 
    
    (* Timers and Filtering *)
    tPreheatTimer       : TON;
    tRunawayTimer       : TON;
    tScraperInterval    : TON;
    rTempFilt           : REAL := 0.0;
    rPressFilt          : REAL := 0.0;
    
    (* PID State *)
    rPressError         : REAL;
    rPressInteg         : REAL := 0.0;
    rPressKp            : REAL := 25.0;
    rPressKi            : REAL := 2.5;
    
    (* Constants *)
    c_TempCrit_C        : REAL := 650.0; (* Upper safety limit for reactor wall *)
    c_TempTarget_C      : REAL := 550.0; (* Ideal reaction temperature *)
    c_PressTarget_MPa   : REAL := 25.0;  (* Supercritical operating pressure *)
    c_PressCrit_MPa     : REAL := 30.0;  (* Maximum pressure limit *)
    c_AlphaFilt         : REAL := 0.2;   (* First-order filter coefficient *)
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety Interlocks and Hard Stops *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bCriticalAlarm := TRUE;
    bQuenchActivate := TRUE;  (* Fail-safe quench dump *)
    rLetdownValve1_Pos := 100.0; (* Depressurize *)
    rLetdownValve2_Pos := 100.0; 
    bScraperMotorRun := FALSE;
    rHeaterCmd_kW := 0.0;
    iScwoState := 99; (* FAULT STATE *)
    RETURN;
END_IF;

(* 2. Sensor Filtering (First-order EWMA for high-noise environment) *)
rTempFilt := (c_AlphaFilt * rReactorTemp_C) + ((1.0 - c_AlphaFilt) * rTempFilt);
rPressFilt := (c_AlphaFilt * rReactorPress_MPa) + ((1.0 - c_AlphaFilt) * rPressFilt);

(* 3. Thermal Runaway Detection *)
IF rTempFilt > c_TempCrit_C OR rPressFilt > c_PressCrit_MPa THEN
    tRunawayTimer(IN := TRUE, PT := T#500MS);
    IF tRunawayTimer.Q THEN
        bCriticalAlarm := TRUE;
        bQuenchActivate := TRUE;
        rLetdownValve1_Pos := 100.0;
        iScwoState := 99; 
    END_IF;
ELSE
    tRunawayTimer(IN := FALSE);
END_IF;

(* 4. Main SCWO State Machine *)
CASE iScwoState OF
    0: (* IDLE & INITIALIZATION *)
        bSystemReady := FALSE;
        bQuenchActivate := FALSE;
        rLetdownValve1_Pos := 0.0;
        rLetdownValve2_Pos := 0.0;
        bScraperMotorRun := FALSE;
        rHeaterCmd_kW := 0.0;
        
        IF bSystemEnable THEN
            iScwoState := 10;
        END_IF;
        
    10: (* PRESSURIZATION & PREHEAT *)
        (* Command preheaters to reach supercritical phase boundary *)
        rHeaterCmd_kW := 150.0; 
        
        (* Cascade pressure control logic setup *)
        rLetdownValve1_Pos := 5.0; (* minimal bleed *)
        rLetdownValve2_Pos := 5.0;
        
        IF rTempFilt > 400.0 AND rPressFilt > 23.0 THEN
            tPreheatTimer(IN := TRUE, PT := T#10S);
            IF tPreheatTimer.Q THEN
                tPreheatTimer(IN := FALSE);
                iScwoState := 20;
            END_IF;
        END_IF;
        
    20: (* STEADY STATE OXIDATION *)
        bSystemReady := TRUE;
        rHeaterCmd_kW := 50.0; (* Maintenance heat, reaction is exothermic *)
        
        (* Cascaded Letdown Valve PI Control *)
        rPressError := rPressFilt - c_PressTarget_MPa;
        rPressInteg := rPressInteg + (rPressError * 0.1); (* Assuming 100ms cycle *)
        
        (* Anti-windup *)
        IF rPressInteg > 50.0 THEN rPressInteg := 50.0; END_IF;
        IF rPressInteg < -50.0 THEN rPressInteg := -50.0; END_IF;
        
        rLetdownValve1_Pos := (rPressKp * rPressError) + (rPressKi * rPressInteg) + 30.0;
        
        (* Clamp outputs *)
        IF rLetdownValve1_Pos > 100.0 THEN rLetdownValve1_Pos := 100.0; END_IF;
        IF rLetdownValve1_Pos < 5.0 THEN rLetdownValve1_Pos := 5.0; END_IF;
        
        (* Valve 2 handles the coarse expansion taking the remaining pressure drop *)
        rLetdownValve2_Pos := rLetdownValve1_Pos * 1.2;
        IF rLetdownValve2_Pos > 100.0 THEN rLetdownValve2_Pos := 100.0; END_IF;
        
        (* Salt Scraper Duty Cycle *)
        tScraperInterval(IN := NOT tScraperInterval.Q, PT := T#30S);
        IF tScraperInterval.ET > T#25S THEN
            bScraperMotorRun := TRUE;
        ELSE
            bScraperMotorRun := FALSE;
        END_IF;

        (* Normal Shutdown *)
        IF NOT bSystemEnable THEN
            iScwoState := 30;
        END_IF;

    30: (* CONTROLLED COOLDOWN *)
        bSystemReady := FALSE;
        rHeaterCmd_kW := 0.0;
        rLetdownValve1_Pos := 50.0; (* Controlled depressurization *)
        rLetdownValve2_Pos := 50.0;
        
        IF rTempFilt < 100.0 AND rPressFilt < 1.0 THEN
            iScwoState := 0;
        END_IF;
        
    99: (* FAULT HANDLING *)
        (* Requires manual reset via bSystemEnable toggle after faults clear *)
        IF NOT bCriticalAlarm AND NOT bSystemEnable THEN
            iScwoState := 0;
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

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
