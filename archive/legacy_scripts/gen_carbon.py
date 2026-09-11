import json, uuid
import os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Advanced Carbon Fiber Oxidation Oven**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 12-zone cascading temperature loops, extreme exothermic reaction runaway prevention, precise PAN precursor tensioning, and toxic off-gas extraction). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_CarbonFiberOxidation\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Advanced Carbon Fiber Oxidation Oven

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.
</USER_REQUEST>"""

code = """```iec-st
FUNCTION_BLOCK FB_AdvancedCarbonFiberOxidationOven
VAR_INPUT
    (* Core Enable & Safety *)
    bEnable                 : BOOL;     (* Main Enable for Oxidation process *)
    bEStopOK                : BOOL;     (* Emergency Stop Relay Status, TRUE = OK *)
    bFireSuppression        : BOOL;     (* Fire suppression active signal *)
    
    (* Process Variables (Temperatures for 12 zones) *)
    arZoneTempAct           : ARRAY[1..12] OF REAL; (* Actual Zone Temperatures [deg C] *)
    
    (* PAN Precursor Tension Control *)
    rInletTensionAct        : REAL;     (* Precursor inlet tension [N] *)
    rOutletTensionAct       : REAL;     (* Precursor outlet tension [N] *)
    rLineSpeedAct           : REAL;     (* Current line speed [m/min] *)
    
    (* Off-gas Extraction *)
    rExhaustFlowAct         : REAL;     (* Exhaust air flow rate [m3/h] *)
    rHCNConcentration       : REAL;     (* Hydrogen Cyanide concentration [ppm] *)
END_VAR
VAR_OUTPUT
    (* Status & Safety *)
    bSystemReady            : BOOL;     (* Overall system ready to process material *)
    bProcessActive          : BOOL;     (* Process is actively running *)
    bThermalRunawayAlarm    : BOOL;     (* Critical exothermic runaway detected *)
    bToxicGasAlarm          : BOOL;     (* HCN or other off-gas limit exceeded *)
    
    (* Control Outputs *)
    arZoneTempCmd           : ARRAY[1..12] OF REAL; (* Heater/Cooler command [%] *)
    rInletTensionCmd        : REAL;     (* Inlet tensioner motor torque command [%] *)
    rOutletTensionCmd       : REAL;     (* Outlet tensioner motor torque command [%] *)
    rExhaustFanVFD          : REAL;     (* Exhaust fan speed command [%] *)
END_VAR
VAR
    (* Internal State & Timers *)
    iState                  : INT := 0; (* 0=Idle, 10=Purge, 20=HeatUp, 30=Run, 99=Fault *)
    tPurgeTimer             : TON;
    tRampTimer              : TON;
    
    (* PID Controllers (Simulated) *)
    rTensionError           : REAL;
    rTensionIntegral        : REAL;
    
    (* Exothermic Management Variables *)
    i                       : INT;
    rMaxTempDelta           : REAL;
    arZoneTempSetpt         : ARRAY[1..12] OF REAL := [210.0, 220.0, 230.0, 240.0, 245.0, 250.0, 255.0, 260.0, 265.0, 270.0, 275.0, 280.0];
END_VAR

(* === MAIN SAFETY INTERLOCKS === *)
IF NOT bEStopOK OR bFireSuppression THEN
    bSystemReady := FALSE;
    bProcessActive := FALSE;
    bThermalRunawayAlarm := bFireSuppression;
    rExhaustFanVFD := 100.0; (* Max exhaust on safety trip *)
    
    (* Shutdown all heaters *)
    FOR i := 1 TO 12 DO
        arZoneTempCmd[i] := 0.0;
    END_FOR;
    
    rInletTensionCmd := 0.0;
    rOutletTensionCmd := 0.0;
    iState := 99;
    RETURN;
END_IF;

(* Continuous Gas Monitoring *)
IF rHCNConcentration > 50.0 THEN
    bToxicGasAlarm := TRUE;
    rExhaustFanVFD := 100.0;
ELSE
    bToxicGasAlarm := FALSE;
END_IF;

(* Exothermic Runaway Detection (Delta T / Delta t simulation) *)
rMaxTempDelta := 0.0;
FOR i := 1 TO 12 DO
    IF (arZoneTempAct[i] - arZoneTempSetpt[i]) > rMaxTempDelta THEN
        rMaxTempDelta := arZoneTempAct[i] - arZoneTempSetpt[i];
    END_IF;
END_FOR;

IF rMaxTempDelta > 15.0 THEN
    bThermalRunawayAlarm := TRUE;
    iState := 99; (* Transition to fault *)
ELSE
    bThermalRunawayAlarm := FALSE;
END_IF;

(* === STATE MACHINE === *)
CASE iState OF
    0: (* IDLE *)
        bSystemReady := TRUE;
        bProcessActive := FALSE;
        rExhaustFanVFD := 20.0; (* Maintain slight negative pressure *)
        
        IF bEnable AND NOT bThermalRunawayAlarm AND NOT bToxicGasAlarm THEN
            iState := 10;
        END_IF;

    10: (* PURGE & VENTILATION PROVE *)
        bSystemReady := FALSE;
        rExhaustFanVFD := 80.0;
        
        tPurgeTimer(IN := TRUE, PT := T#30S);
        
        IF tPurgeTimer.Q THEN
            IF rExhaustFlowAct > 5000.0 THEN (* Validate flow *)
                tPurgeTimer(IN := FALSE);
                iState := 20;
            ELSE
                (* Fail to establish draft *)
                iState := 99;
            END_IF;
        END_IF;

    20: (* HEAT UP ZONE CASCADE *)
        (* Basic ramp logic simulation *)
        tRampTimer(IN := TRUE, PT := T#5S);
        IF tRampTimer.Q THEN
            tRampTimer(IN := FALSE);
        END_IF;
        
        (* Simple P-control for heaters *)
        FOR i := 1 TO 12 DO
            IF arZoneTempAct[i] < arZoneTempSetpt[i] THEN
                arZoneTempCmd[i] := (arZoneTempSetpt[i] - arZoneTempAct[i]) * 5.0; 
                IF arZoneTempCmd[i] > 100.0 THEN arZoneTempCmd[i] := 100.0; END_IF;
            ELSE
                arZoneTempCmd[i] := 0.0; (* Rely on process to cool or activate cooling loop *)
            END_IF;
        END_FOR;
        
        (* Transition to run if first zone is at temp *)
        IF arZoneTempAct[1] >= (arZoneTempSetpt[1] - 2.0) THEN
            iState := 30;
        END_IF;
        
    30: (* PROCESS RUNNING *)
        bProcessActive := TRUE;
        
        (* Maintain tension via PI loop (simplified) *)
        rTensionError := 1500.0 - rOutletTensionAct; (* Target 1500N *)
        rTensionIntegral := rTensionIntegral + (rTensionError * 0.01);
        rOutletTensionCmd := (rTensionError * 0.5) + rTensionIntegral;
        
        IF rOutletTensionCmd > 100.0 THEN rOutletTensionCmd := 100.0; END_IF;
        IF rOutletTensionCmd < 0.0 THEN rOutletTensionCmd := 0.0; END_IF;
        
        (* Adjust inlet to maintain differential tension based on line speed *)
        rInletTensionCmd := rOutletTensionCmd * 0.8; 
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    99: (* FAULT / SAFE STATE *)
        bSystemReady := FALSE;
        bProcessActive := FALSE;
        rExhaustFanVFD := 100.0;
        rInletTensionCmd := 0.0;
        rOutletTensionCmd := 0.0;
        FOR i := 1 TO 12 DO
            arZoneTempCmd[i] := 0.0;
        END_FOR;
        
        IF NOT bEnable AND bEStopOK AND NOT bFireSuppression AND NOT bThermalRunawayAlarm THEN
            iState := 0; (* Reset fault if enable dropped and clear *)
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
