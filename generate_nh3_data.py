import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Next-Gen Heavy-Duty Marine Dual-Fuel Ammonia (NH3) Engine**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., High-pressure ammonia direct injection micro-pilot diesel ignition, selective catalytic reduction (SCR) unburnt slip mitigation, and double-wall pipe purge gas monitoring). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_AmmoniaMarineEngine\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Next-Gen Heavy-Duty Marine Dual-Fuel Ammonia (NH3) Engine

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_NH3_DualFuelMarineEngineCtrl
VAR_INPUT
    (* Safety and Enable Signals *)
    bSystemEnable       : BOOL;     (* Main propulsion enable signal *)
    bEmergencyStop      : BOOL;     (* E-stop chain OK signal *)
    bLeakDetectNH3      : BOOL;     (* Ammonia leak detected in double-wall pipe *)
    
    (* Process Variables *)
    rEngineSpeedRPM     : REAL;     (* Engine speed in RPM *)
    rLoadDemand         : REAL;     (* Load demand 0.0 to 100.0% *)
    rNH3HeaderPressure  : REAL;     (* Ammonia rail pressure in bar (target ~600 bar) *)
    rDieselPilotPress   : REAL;     (* Diesel micro-pilot pressure in bar *)
    rSCRTempInlet       : REAL;     (* SCR inlet temperature in deg C *)
END_VAR

VAR_OUTPUT
    (* Status and Alarms *)
    bReadyForAmmonia    : BOOL;     (* Engine ready to transition to NH3 mode *)
    bOperatingNH3       : BOOL;     (* Currently operating in NH3 mode *)
    bCriticalAlarm      : BOOL;     (* Engine shutdown or critical safety fault *)
    bPurgeValveOpen     : BOOL;     (* Command to open N2 purge valves on double-walled pipes *)
    
    (* Control Signals *)
    rNH3InjectionQty    : REAL;     (* Commanded NH3 injection quantity (mg/stroke) *)
    rDieselPilotQty     : REAL;     (* Commanded Diesel pilot quantity (mg/stroke) *)
    rUreaDosingRate     : REAL;     (* SCR Urea dosing rate to mitigate NH3 slip (kg/hr) *)
END_VAR

VAR
    (* Internal State *)
    iOperationState     : INT := 0; (* 0:IDLE, 10:DIESEL_ONLY, 20:TRANSITION, 30:DUAL_FUEL, 99:FAULT *)
    tPurgeTimer         : TON;      (* Timer for N2 purge sequence *)
    tTransitionTimer    : TON;      (* Timer for mode transitions *)
    rNH3SlipEstimate    : REAL;     (* Estimated unburnt NH3 slip in ppm *)
END_VAR

(* === MAIN LOGIC === *)

(* Safety Interlocks *)
IF NOT bEmergencyStop OR bLeakDetectNH3 THEN
    bCriticalAlarm := TRUE;
    bOperatingNH3 := FALSE;
    rNH3InjectionQty := 0.0;
    rDieselPilotQty := 0.0;
    iOperationState := 99;
    
    (* If leak detected, initiate double-wall purge *)
    IF bLeakDetectNH3 THEN
        bPurgeValveOpen := TRUE;
    END_IF;
    RETURN;
END_IF;

(* SCR Temperature check for Ammonia operation *)
IF rSCRTempInlet > 280.0 THEN
    bReadyForAmmonia := TRUE;
ELSE
    bReadyForAmmonia := FALSE;
END_IF;

CASE iOperationState OF
    0: (* IDLE *)
        bOperatingNH3 := FALSE;
        rNH3InjectionQty := 0.0;
        rDieselPilotQty := 0.0;
        IF bSystemEnable AND (rLoadDemand > 5.0) THEN
            iOperationState := 10;
        END_IF;

    10: (* DIESEL ONLY MODE *)
        bOperatingNH3 := FALSE;
        rNH3InjectionQty := 0.0;
        rDieselPilotQty := rLoadDemand * 2.5; (* Base diesel mapping *)
        
        IF bReadyForAmmonia AND (rLoadDemand > 30.0) AND (rNH3HeaderPressure > 550.0) THEN
            tTransitionTimer(IN := TRUE, PT := T#10S);
            IF tTransitionTimer.Q THEN
                tTransitionTimer(IN := FALSE);
                iOperationState := 20;
            END_IF;
        ELSE
            tTransitionTimer(IN := FALSE);
        END_IF;

    20: (* TRANSITION TO DUAL FUEL *)
        bOperatingNH3 := TRUE;
        (* Ramp up NH3, ramp down Diesel *)
        rNH3InjectionQty := rLoadDemand * 1.5; 
        rDieselPilotQty := 5.0; (* Micro-pilot minimum *)
        
        IF rNH3InjectionQty > 20.0 THEN
            iOperationState := 30;
        END_IF;

    30: (* DUAL FUEL (NH3 MAIN) *)
        bOperatingNH3 := TRUE;
        rDieselPilotQty := 3.0; (* Micro-pilot ignition *)
        rNH3InjectionQty := rLoadDemand * 3.8; (* Main energy source *)
        
        (* NH3 Slip Mitigation (SCR Control) *)
        rNH3SlipEstimate := rNH3InjectionQty * 0.02; (* Simple physical model for slip *)
        rUreaDosingRate := rNH3SlipEstimate * 1.2;
        
        IF rLoadDemand < 20.0 THEN
            iOperationState := 10; (* Revert to diesel at low loads *)
        END_IF;

    99: (* FAULT STATE *)
        (* Wait for manual reset, handle purge timer *)
        IF bPurgeValveOpen THEN
            tPurgeTimer(IN := TRUE, PT := T#5M);
            IF tPurgeTimer.Q THEN
                bPurgeValveOpen := FALSE;
                tPurgeTimer(IN := FALSE);
            END_IF;
        END_IF;
        
        IF NOT bLeakDetectNH3 AND bEmergencyStop AND NOT bSystemEnable THEN
            bCriticalAlarm := FALSE;
            iOperationState := 0;
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
