import json, uuid, os

prompt = """<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Continuous Polyethylene Terephthalate (PET) Solid State Polycondensation (SSP) Reactor**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., hot nitrogen counter-current mass flow fluidization, crystalline density gradient tracking, and rotary valve precise throughput metering). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_PET_SSP_Reactor\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Continuous Polyethylene Terephthalate (PET) Solid State Polycondensation (SSP) Reactor

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.
</USER_REQUEST>"""

code = """```iec-st
FUNCTION_BLOCK FB_PET_SSP_Reactor
VAR_INPUT
    bSystemEnable           : BOOL;     (* Global Enable Signal for the SSP Reactor System *)
    bEmergencyStop          : BOOL;     (* Safety Relay Status (FALSE = E-Stop Active) *)
    rInletPelletTemp        : REAL;     (* Pre-crystallized PET pellet inlet temperature [deg C] *)
    rN2GasMassFlow          : REAL;     (* Counter-current Hot N2 mass flow rate [kg/h] *)
    rN2InletTemp            : REAL;     (* Hot N2 inlet temperature at bottom of reactor [deg C] *)
    rTargetIntrinsicVisc    : REAL;     (* Target Intrinsic Viscosity (IV) for final PET product [dL/g] *)
    rLevelMeasurement       : REAL;     (* Radar level measurement of PET bed [m] *)
    bDischargePermit        : BOOL;     (* Downstream process ready to accept product *)
END_VAR
VAR_OUTPUT
    bReactorReady           : BOOL;     (* Reactor in steady state and producing on-spec IV *)
    rRotaryValveSpeedSetp   : REAL;     (* Discharge rotary valve speed setpoint [RPM] *)
    rN2HeaterPower          : REAL;     (* Nitrogen heater SCR power control [0-100%] *)
    bHighTempAlarm          : BOOL;     (* Alarm: Reactor bed temperature exceeded safety limits *)
    bChokingAlarm           : BOOL;     (* Alarm: Potential fluidization choking detected *)
    rEstimatedIV            : REAL;     (* Real-time model estimation of current discharge IV [dL/g] *)
END_VAR
VAR
    iState                  : INT := 0; (* State Machine Index *)
    rBedDensity             : REAL;     (* Estimated bulk density of the crystallizing bed [kg/m^3] *)
    rResidenceTime          : REAL;     (* Calculated average residence time [h] *)
    rReactionRate           : REAL;     (* SSP Reaction rate constant dependent on temperature *)
    rCurrentIV              : REAL := 0.60; (* Inlet IV starts at base pre-polymer level *)
    tStartupDelay           : TON;      (* Delay timer for heating system stabilization *)
    tUpdateRate             : TON;      (* Kinetic model calculation frequency *)
    
    (* Internal PID variables *)
    rLevelError             : REAL;
    rIntegralTerm           : REAL := 0.0;
    rKp                     : REAL := 2.5;
    rKi                     : REAL := 0.05;
    rMaxSpeed               : REAL := 50.0;
END_VAR

(* === MAIN LOGIC === *)
IF NOT bEmergencyStop THEN
    bReactorReady := FALSE;
    bHighTempAlarm := FALSE;
    bChokingAlarm := FALSE;
    rRotaryValveSpeedSetp := 0.0;
    rN2HeaterPower := 0.0;
    iState := 0;
    RETURN;
END_IF;

(* Continuous Kinetic Model Update (Runs every 1 second) *)
tUpdateRate(IN := TRUE, PT := T#1S);
IF tUpdateRate.Q THEN
    tUpdateRate(IN := FALSE);
    
    (* Calculate Arrhenius-based SSP reaction rate constant k(T) *)
    (* Assuming base activation energy and universal gas constant parameters *)
    rReactionRate := EXP(-15000.0 / (rN2InletTemp + 273.15)) * 1.5E6;
    
    (* Estimate local bed density change as a function of temperature and IV *)
    rBedDensity := 850.0 + (rN2InletTemp - 200.0) * 0.5 + (rCurrentIV - 0.6) * 100.0;
    
    (* Calculate dynamic residence time based on level and throughput *)
    IF rRotaryValveSpeedSetp > 0.0 THEN
        rResidenceTime := (rLevelMeasurement * 3.14 * 2.0 * rBedDensity) / (rRotaryValveSpeedSetp * 15.0);
    ELSE
        rResidenceTime := 10.0; (* Nominal hold time during stagnant conditions *)
    END_IF;
    
    (* Update real-time estimated IV based on residence time and reaction rate *)
    rEstimatedIV := rCurrentIV + (rReactionRate * rResidenceTime * 0.1);
END_IF;

(* State Machine for Reactor Operation *)
CASE iState OF
    0: (* SYSTEM IDLE / OFF *)
        bReactorReady := FALSE;
        rRotaryValveSpeedSetp := 0.0;
        rN2HeaterPower := 0.0;
        IF bSystemEnable THEN
            iState := 10;
        END_IF;

    10: (* HEATING N2 GAS *)
        (* Ramp up Nitrogen heater power proportional to required temperature delta *)
        rN2HeaterPower := (210.0 - rN2InletTemp) * 1.2;
        IF rN2HeaterPower > 100.0 THEN rN2HeaterPower := 100.0; END_IF;
        IF rN2HeaterPower < 0.0 THEN rN2HeaterPower := 0.0; END_IF;
        
        tStartupDelay(IN := (rN2InletTemp >= 205.0), PT := T#5M);
        IF tStartupDelay.Q THEN
            tStartupDelay(IN := FALSE);
            iState := 20;
        END_IF;
        IF NOT bSystemEnable THEN iState := 0; END_IF;

    20: (* CONTINUOUS PRODUCTION *)
        (* Maintain N2 Temperature *)
        rN2HeaterPower := 50.0 + (210.0 - rN2InletTemp) * 2.0;
        IF rN2HeaterPower > 100.0 THEN rN2HeaterPower := 100.0; END_IF;
        IF rN2HeaterPower < 0.0 THEN rN2HeaterPower := 0.0; END_IF;
        
        (* Level Control PID -> Rotary Valve Speed *)
        rLevelError := rLevelMeasurement - 12.0; (* Target bed height = 12m *)
        rIntegralTerm := rIntegralTerm + (rLevelError * rKi);
        
        IF bDischargePermit THEN
            rRotaryValveSpeedSetp := (rLevelError * rKp) + rIntegralTerm;
            IF rRotaryValveSpeedSetp > rMaxSpeed THEN rRotaryValveSpeedSetp := rMaxSpeed; END_IF;
            IF rRotaryValveSpeedSetp < 0.0 THEN rRotaryValveSpeedSetp := 0.0; END_IF;
        ELSE
            rRotaryValveSpeedSetp := 0.0;
        END_IF;
        
        (* Evaluate Quality & Safety Alarms *)
        IF rN2InletTemp > 225.0 THEN
            bHighTempAlarm := TRUE;
        ELSE
            bHighTempAlarm := FALSE;
        END_IF;
        
        IF rN2GasMassFlow > 5000.0 AND rBedDensity < 800.0 THEN
            bChokingAlarm := TRUE;
        ELSE
            bChokingAlarm := FALSE;
        END_IF;
        
        IF rEstimatedIV >= rTargetIntrinsicVisc AND NOT bHighTempAlarm THEN
            bReactorReady := TRUE;
        ELSE
            bReactorReady := FALSE;
        END_IF;
        
        IF NOT bSystemEnable THEN 
            iState := 0; 
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
