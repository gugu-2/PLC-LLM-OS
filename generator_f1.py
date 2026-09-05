import json, uuid, os

os.makedirs('data/swarm_raw', exist_ok=True)

prompt = """<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Formula 1 Composite Autoclave Curing System**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., multi-zone vacuum bagging pressure control, precise ramp-soak temperature profiling, exothermic delta-T management, and nitrogen purging logic). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_CompositeAutoclave\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Formula 1 Composite Autoclave Curing System

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.
</USER_REQUEST>"""

code = """```iec-st
FUNCTION_BLOCK FB_F1CompositeAutoclave
VAR_INPUT
    (* Main System Commands and Safety *)
    bSystemEnable       : BOOL;     (* Main system enable for autoclave operations *)
    bEmergencyStop      : BOOL;     (* Safety relay OK signal - active HIGH means safe *)
    bStartCycle         : BOOL;     (* Command to start the curing cycle *)
    
    (* Process Variables (Analog Inputs) *)
    rVesselPressure     : REAL;     (* Current vessel pressure in bar (absolute) *)
    rNitrogenSupply     : REAL;     (* Nitrogen supply pressure in bar *)
    rZone1Temp          : REAL;     (* Temperature of heating zone 1 in deg C *)
    rZone2Temp          : REAL;     (* Temperature of heating zone 2 in deg C *)
    rZone3Temp          : REAL;     (* Temperature of heating zone 3 in deg C *)
    rPartTempLead       : REAL;     (* Leading thermocouple on the carbon part (deg C) *)
    rPartTempLag        : REAL;     (* Lagging thermocouple on the carbon part (deg C) *)
    rVacuumBagPress     : REAL;     (* Vacuum bag pressure in mbar (absolute) *)
END_VAR
VAR_OUTPUT
    (* Status Indicators *)
    bSystemReady        : BOOL;     (* Autoclave ready to commence curing cycle *)
    bCycleActive        : BOOL;     (* Curing cycle is currently active *)
    bCriticalAlarm      : BOOL;     (* Exothermic runaway, pressure loss, or estop alarm *)
    iCurrentPhase       : INT;      (* Current curing phase (0: Idle, 10: Purge, 20: Ramp, 30: Soak, 40: Cool) *)
    
    (* Actuator Control Commands (Analog Outputs) *)
    rHeaterCmdZone1     : REAL;     (* Command output for Zone 1 Thyristor (0-100%) *)
    rHeaterCmdZone2     : REAL;     (* Command output for Zone 2 Thyristor (0-100%) *)
    rHeaterCmdZone3     : REAL;     (* Command output for Zone 3 Thyristor (0-100%) *)
    rN2PurgeValveCmd    : REAL;     (* Nitrogen proportional purge valve command (0-100%) *)
    rVacuumPumpCmd      : REAL;     (* Vacuum pump VFD command (0-100%) *)
END_VAR
VAR
    (* Internal state variables *)
    iState              : INT := 0;
    tPhaseTimer         : TON;
    tCycleTimer         : TON;
    
    (* Recipe parameters for F1 composite part *)
    rTargetRampRate     : REAL := 2.5; (* degC per minute *)
    rTargetSoakTemp     : REAL := 180.0; (* Prepreg curing soak temp *)
    rDeltaTLimit        : REAL := 15.0; (* Max allowable delta T across part *)
    
    (* Control loop variables *)
    rCurrentSetpoint    : REAL := 25.0;
    bExothermicCondition: BOOL := FALSE;
    bVacuumLoss         : BOOL := FALSE;
    rAveragePartTemp    : REAL := 0.0;
END_VAR

(* === MAIN LOGIC === *)

(* 1. Safety & Interlocks *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bCycleActive := FALSE;
    bCriticalAlarm := TRUE;
    rHeaterCmdZone1 := 0.0;
    rHeaterCmdZone2 := 0.0;
    rHeaterCmdZone3 := 0.0;
    rN2PurgeValveCmd := 0.0;
    rVacuumPumpCmd := 0.0;
    iState := 999; (* Error State *)
    RETURN;
END_IF;

(* Calculate Average Part Temp *)
rAveragePartTemp := (rPartTempLead + rPartTempLag) / 2.0;

(* 2. Exothermic & Vacuum Integrity Monitoring *)
(* Check if part is heating significantly faster than setpoint (exothermic reaction of resin) *)
IF (rPartTempLead - rCurrentSetpoint) > 10.0 THEN
    bExothermicCondition := TRUE;
ELSE
    bExothermicCondition := FALSE;
END_IF;

(* Check for vacuum bag leak during pressure phases *)
IF (rVacuumBagPress > 200.0) AND (iState >= 20) AND (iState < 50) THEN
    bVacuumLoss := TRUE;
ELSE
    bVacuumLoss := FALSE;
END_IF;

IF bExothermicCondition OR bVacuumLoss THEN
    bCriticalAlarm := TRUE;
    iState := 999; (* Fast Abort *)
END_IF;

(* 3. State Machine for Curing Cycle *)
CASE iState OF
    0: (* IDLE *)
        iCurrentPhase := 0;
        bSystemReady := TRUE;
        bCycleActive := FALSE;
        rHeaterCmdZone1 := 0.0;
        rHeaterCmdZone2 := 0.0;
        rHeaterCmdZone3 := 0.0;
        rN2PurgeValveCmd := 0.0;
        rVacuumPumpCmd := 0.0;
        
        IF bSystemEnable AND bStartCycle THEN
            bSystemReady := FALSE;
            bCycleActive := TRUE;
            bCriticalAlarm := FALSE;
            rCurrentSetpoint := rAveragePartTemp; (* Start ramp from current temp *)
            iState := 10;
        END_IF;

    10: (* PURGE & VACUUM ESTABLISHMENT *)
        iCurrentPhase := 10;
        rVacuumPumpCmd := 100.0;
        rN2PurgeValveCmd := 80.0; (* Fast Nitrogen purge to remove oxygen *)
        tPhaseTimer(IN := TRUE, PT := T#5M);
        
        IF tPhaseTimer.Q AND (rVacuumBagPress < 50.0) THEN
            tPhaseTimer(IN := FALSE);
            rN2PurgeValveCmd := 10.0; (* Maintain slight overpressure flow *)
            iState := 20;
        END_IF;

    20: (* RAMP TO SOAK *)
        iCurrentPhase := 20;
        
        (* Ramp generation: Assuming 100ms cycle time, increase setpoint based on rate per minute *)
        rCurrentSetpoint := rCurrentSetpoint + (rTargetRampRate / 600.0); 
        IF rCurrentSetpoint > rTargetSoakTemp THEN
            rCurrentSetpoint := rTargetSoakTemp;
        END_IF;
        
        (* Thermal control loop: Proportional response to error *)
        rHeaterCmdZone1 := (rCurrentSetpoint - rZone1Temp) * 2.5;
        rHeaterCmdZone2 := (rCurrentSetpoint - rZone2Temp) * 2.5;
        rHeaterCmdZone3 := (rCurrentSetpoint - rZone3Temp) * 2.5;
        
        (* Clamp outputs between 0 and 100% *)
        IF rHeaterCmdZone1 > 100.0 THEN rHeaterCmdZone1 := 100.0; ELSIF rHeaterCmdZone1 < 0.0 THEN rHeaterCmdZone1 := 0.0; END_IF;
        IF rHeaterCmdZone2 > 100.0 THEN rHeaterCmdZone2 := 100.0; ELSIF rHeaterCmdZone2 < 0.0 THEN rHeaterCmdZone2 := 0.0; END_IF;
        IF rHeaterCmdZone3 > 100.0 THEN rHeaterCmdZone3 := 100.0; ELSIF rHeaterCmdZone3 < 0.0 THEN rHeaterCmdZone3 := 0.0; END_IF;

        (* Advance to soak once lagging part temperature reaches soak target minus tolerance *)
        IF rPartTempLag >= (rTargetSoakTemp - 2.0) THEN
            iState := 30;
        END_IF;

    30: (* SOAK / CURE *)
        iCurrentPhase := 30;
        tPhaseTimer(IN := TRUE, PT := T#120M); (* 2 hours soak for carbon fiber prepreg *)
        
        (* Maintain soak temperature with tighter proportional gain *)
        rHeaterCmdZone1 := (rTargetSoakTemp - rZone1Temp) * 1.5;
        rHeaterCmdZone2 := (rTargetSoakTemp - rZone2Temp) * 1.5;
        rHeaterCmdZone3 := (rTargetSoakTemp - rZone3Temp) * 1.5;
        
        IF rHeaterCmdZone1 > 100.0 THEN rHeaterCmdZone1 := 100.0; ELSIF rHeaterCmdZone1 < 0.0 THEN rHeaterCmdZone1 := 0.0; END_IF;
        IF rHeaterCmdZone2 > 100.0 THEN rHeaterCmdZone2 := 100.0; ELSIF rHeaterCmdZone2 < 0.0 THEN rHeaterCmdZone2 := 0.0; END_IF;
        IF rHeaterCmdZone3 > 100.0 THEN rHeaterCmdZone3 := 100.0; ELSIF rHeaterCmdZone3 < 0.0 THEN rHeaterCmdZone3 := 0.0; END_IF;

        IF tPhaseTimer.Q THEN
            tPhaseTimer(IN := FALSE);
            iState := 40;
        END_IF;

    40: (* COOLING *)
        iCurrentPhase := 40;
        
        (* Disable heaters for cooling phase *)
        rHeaterCmdZone1 := 0.0;
        rHeaterCmdZone2 := 0.0;
        rHeaterCmdZone3 := 0.0;
        
        (* Gradual ramp down of setpoint for controlled cooling *)
        rCurrentSetpoint := rCurrentSetpoint - 1.5; 
        
        (* Safe to open vessel when part is cool enough *)
        IF rPartTempLead < 40.0 THEN
            rVacuumPumpCmd := 0.0;
            rN2PurgeValveCmd := 0.0;
            iState := 50;
        END_IF;

    50: (* CYCLE COMPLETE *)
        iCurrentPhase := 50;
        bCycleActive := FALSE;
        bSystemReady := TRUE;
        
        (* Wait for operator to clear the cycle command *)
        IF NOT bStartCycle THEN
            iState := 0;
        END_IF;
        
    999: (* FAULT HANDLING *)
        bCycleActive := FALSE;
        rHeaterCmdZone1 := 0.0;
        rHeaterCmdZone2 := 0.0;
        rHeaterCmdZone3 := 0.0;
        
        (* In case of exothermic reaction, pump in cold N2 to quench *)
        IF bExothermicCondition THEN
            rN2PurgeValveCmd := 100.0;
        ELSE
            rN2PurgeValveCmd := 0.0;
        END_IF;
        
        rVacuumPumpCmd := 0.0;
        
        (* Require operator to reset by toggling system enable after alarm clears *)
        IF NOT bSystemEnable THEN
            iState := 0;
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
