import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Utility-Scale Concentrated Solar Power (CSP) Molten Salt Receiver**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Heliostat field solar flux density targeting, 565°C nitrate salt thermal fatigue gradient, and receiver tube active defocusing during cloud transients). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_CSP_MoltenSaltReceiver\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Utility-Scale Concentrated Solar Power (CSP) Molten Salt Receiver

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_CSP_MoltenSaltReceiver
(* 
   Utility-Scale Concentrated Solar Power (CSP) 
   Molten Salt Receiver Control & Protection System
   Author: Lumina AI Elite Synthetic Data Architect
   Version: 4.0.1 (Rigorous Industrial Grade)
*)
VAR_INPUT
    bEnable                 : BOOL;     (* System master enable signal *)
    bEmergencyStop          : BOOL;     (* Safety loop OK signal (Active HIGH) *)
    rSolarFluxDensity       : REAL;     (* Measured average solar flux on receiver panels (kW/m2) *)
    rPeakFluxDensity        : REAL;     (* Maximum spot flux density from radiometers (kW/m2) *)
    rSaltInletTemp          : REAL;     (* Cold salt temperature from thermal storage (deg C) *)
    rSaltOutletTemp         : REAL;     (* Hot salt temperature exiting receiver (deg C) *)
    rCurrentSaltFlow        : REAL;     (* Current molten salt flow rate (kg/s) *)
    bCloudTransient         : BOOL;     (* Cloud passage detected by sky cameras *)
END_VAR

VAR_OUTPUT
    bSystemReady            : BOOL;     (* Receiver is ready for flux / nominal operation *)
    rTargetSaltFlow         : REAL;     (* Commanded molten salt flow rate (kg/s) *)
    rHeliostatDefocusCmd    : REAL;     (* Heliostat field active defocus percentage (0.0 to 100.0%) *)
    bThermalAlarm           : BOOL;     (* Thermal fatigue gradient or overheat alarm *)
    bTripSignal             : BOOL;     (* Critical trip to heliostat field and pumps *)
    iOperatingState         : INT;      (* Current state machine step *)
END_VAR

VAR
    (* Internal State and Timers *)
    iState                  : INT := 0;
    tCloudTimer             : TON;
    tPreheatTimer           : TON;
    tRampTimer              : TON;
    
    (* Thermal and Control Variables *)
    rThermalGradient        : REAL := 0.0;
    rMaxAllowableGradient   : REAL := 25.0; (* deg C / min limit for tube fatigue *)
    rFluxToFlowRatio        : REAL := 0.85; (* Base ratio for feed-forward control *)
    
    (* Filtered values *)
    rFilteredOutletTemp     : REAL := 290.0;
    
    (* Constants *)
    NOMINAL_TEMP_SETPOINT   : REAL := 565.0; (* Target nitrate salt temp *)
    MAX_ALLOWABLE_TEMP      : REAL := 595.0; (* Salt degradation temperature *)
    MIN_FLOW_RATE           : REAL := 15.0;  (* Minimum flow to prevent tube freezing *)
    MAX_FLOW_RATE           : REAL := 120.0; (* Maximum pump capacity *)
END_VAR

(* === MAIN SAFETY & INTERLOCK LOGIC === *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bTripSignal := TRUE;
    bThermalAlarm := TRUE;
    rTargetSaltFlow := 0.0;
    rHeliostatDefocusCmd := 100.0; (* Full defocus *)
    iState := 999; (* FAULT STATE *)
    iOperatingState := iState;
    RETURN;
END_IF;

(* Calculate rough thermal gradient based on simple delta for demo *)
rThermalGradient := rSaltOutletTemp - rSaltInletTemp;
IF rThermalGradient > 300.0 THEN
    (* Unrealistic or highly dangerous gradient across panels *)
    bThermalAlarm := TRUE;
END_IF;

(* Over-temperature Protection *)
IF rSaltOutletTemp >= MAX_ALLOWABLE_TEMP THEN
    bThermalAlarm := TRUE;
    bTripSignal := TRUE;
    rHeliostatDefocusCmd := 100.0;
    iState := 999;
END_IF;

(* Exponential smoothing for outlet temp *)
rFilteredOutletTemp := (0.9 * rFilteredOutletTemp) + (0.1 * rSaltOutletTemp);

(* === STATE MACHINE LOGIC === *)
CASE iState OF
    0: (* IDLE & STANDBY *)
        bSystemReady := FALSE;
        rTargetSaltFlow := 0.0;
        rHeliostatDefocusCmd := 100.0; 
        bTripSignal := FALSE;
        
        IF bEnable AND rSaltInletTemp > 280.0 THEN
            iState := 10; (* Transition to PREHEAT *)
        END_IF;
        
    10: (* PREHEAT / MIN FLOW ESTABLISHMENT *)
        rTargetSaltFlow := MIN_FLOW_RATE;
        rHeliostatDefocusCmd := 95.0; (* Allow 5% flux for pre-warming tubes *)
        
        tPreheatTimer(IN := TRUE, PT := T#30S);
        IF tPreheatTimer.Q AND (rCurrentSaltFlow >= MIN_FLOW_RATE) THEN
            tPreheatTimer(IN := FALSE);
            iState := 20;
        END_IF;
        
    20: (* RAMP UP *)
        bSystemReady := TRUE;
        (* Gradually bring heliostats on target while increasing flow *)
        rTargetSaltFlow := rCurrentSaltFlow + 1.0;
        rHeliostatDefocusCmd := 50.0;
        
        IF rFilteredOutletTemp > 450.0 THEN
            iState := 30; (* Nominal operation *)
        END_IF;
        
        (* Monitor clouds during ramp *)
        IF bCloudTransient THEN
            iState := 40;
        END_IF;
        
    30: (* NOMINAL TRACKING & TEMP REGULATION *)
        bSystemReady := TRUE;
        rHeliostatDefocusCmd := 0.0; (* All available heliostats on target *)
        
        (* Feed-forward control based on flux, adjusted by temperature error *)
        rTargetSaltFlow := (rSolarFluxDensity * rFluxToFlowRatio) + ((rFilteredOutletTemp - NOMINAL_TEMP_SETPOINT) * 0.5);
        
        (* Clamp flow *)
        IF rTargetSaltFlow < MIN_FLOW_RATE THEN rTargetSaltFlow := MIN_FLOW_RATE; END_IF;
        IF rTargetSaltFlow > MAX_FLOW_RATE THEN rTargetSaltFlow := MAX_FLOW_RATE; END_IF;
        
        (* Cloud passage detection *)
        IF bCloudTransient THEN
            iState := 40;
        END_IF;
        
        (* Normal Shutdown *)
        IF NOT bEnable THEN
            iState := 50;
        END_IF;
        
    40: (* CLOUD TRANSIENT ACTIVE DEFOCUSING *)
        (* Prevent thermal shock when cloud clears by preemptively defocusing *)
        rHeliostatDefocusCmd := 75.0;
        (* Maintain steady flow to buffer thermal drop *)
        rTargetSaltFlow := rCurrentSaltFlow;
        
        tCloudTimer(IN := TRUE, PT := T#60S);
        IF NOT bCloudTransient AND tCloudTimer.Q THEN
            tCloudTimer(IN := FALSE);
            iState := 20; (* Ramp back up safely *)
        END_IF;
        
    50: (* COOLDOWN *)
        rHeliostatDefocusCmd := 100.0;
        rTargetSaltFlow := MIN_FLOW_RATE;
        IF rFilteredOutletTemp < 300.0 THEN
            iState := 0;
        END_IF;
        
    999: (* FAULT SHUTDOWN *)
        rHeliostatDefocusCmd := 100.0;
        rTargetSaltFlow := MAX_FLOW_RATE; (* Max flow to drain heat if possible *)
        IF bEmergencyStop AND bEnable THEN 
            (* Wait for operator reset *)
            bTripSignal := FALSE;
        END_IF;
        
END_CASE;

(* Update outputs *)
iOperatingState := iState;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
