import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Commercial Aerospace Carbon Fiber Prepreg Autoclave Pressure and Curing Temperature Cascade**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Autoclave_Curing\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Commercial Aerospace Carbon Fiber Prepreg Autoclave Pressure and Curing Temperature Cascade

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_AeroAutoclaveCascadeControl
VAR_INPUT
    (* Primary operation and safety interlock inputs *)
    bEnableSequence         : BOOL;      (* Master enable for the cure cycle sequence *)
    bEmergencyStopOK        : BOOL;      (* Safety circuit healthy (TRUE = OK) *)
    bDoorLockedAndSealed    : BOOL;      (* Autoclave door mechanical lock limit switch *)
    bNitrogenSupplyOK       : BOOL;      (* Adequate nitrogen pressure available *)
    
    (* Analog process variables *)
    rAirTempSensor1         : REAL;      (* Primary ambient air temperature inside autoclave [Deg C] *)
    rAirTempSensor2         : REAL;      (* Redundant ambient air temperature [Deg C] *)
    rPartTempSensor         : REAL;      (* Prepreg part surface temperature [Deg C] *)
    rVesselPressure         : REAL;      (* Autoclave internal pressure [Bar] *)
    
    (* Recipe setpoints *)
    rTargetDwellTemp        : REAL;      (* Target curing temperature for carbon fiber [Deg C] *)
    rTargetDwellPressure    : REAL;      (* Target curing pressure [Bar] *)
END_VAR
VAR_OUTPUT
    (* Discrete control outputs *)
    bHeaterContactor        : BOOL;      (* Enable main heater banks *)
    bCoolingFan             : BOOL;      (* Enable cooling circulation fans *)
    bCycleComplete          : BOOL;      (* Indicates successful cure cycle completion *)
    bCriticalFault          : BOOL;      (* Unrecoverable fault, system safely aborting *)
    
    (* Analog control outputs *)
    rHeaterPowerCmd         : REAL;      (* 0.0 - 100.0% heater SCR power demand *)
    rPressureValveCmd       : REAL;      (* 0.0 - 100.0% nitrogen pressurization valve command *)
    rExhaustValveCmd        : REAL;      (* 0.0 - 100.0% exhaust/vent valve command *)
END_VAR
VAR
    (* Internal state variables *)
    iCycleState             : INT := 0;  (* Main state machine step *)
    tDwellTimer             : TON;       (* Timer for curing dwell phase *)
    
    (* Math/Filtering Variables *)
    rAvgAirTemp             : REAL;      (* Filtered average air temperature *)
    
    (* Cascade PID Variables *)
    rTempError              : REAL;      (* Proportional temperature error *)
    rTempIntegral           : REAL;      (* Integral accumulation for temp PID *)
    rPressError             : REAL;      (* Proportional pressure error *)
    rPressIntegral          : REAL;      (* Integral accumulation for pressure PID *)
    
    (* PID Tuning Parameters (Hardcoded for simulation) *)
    Kp_Temp                 : REAL := 2.85;
    Ki_Temp                 : REAL := 0.015;
    Kp_Press                : REAL := 4.20;
    Ki_Press                : REAL := 0.025;
END_VAR

(* === SAFETY & MULTI-LAYERED INTERLOCKS === *)
(* Ensure all critical safety parameters are met before allowing operation.
   If any fails during operation, force system to state 99 for safe abort. *)
IF NOT bEmergencyStopOK OR NOT bDoorLockedAndSealed OR NOT bNitrogenSupplyOK THEN
    bHeaterContactor := FALSE;
    rHeaterPowerCmd := 0.0;
    bCoolingFan := FALSE;
    rPressureValveCmd := 0.0;
    rExhaustValveCmd := 100.0; (* Fail-safe depressurization *)
    iCycleState := 99; (* Fault state *)
    bCriticalFault := TRUE;
    bCycleComplete := FALSE;
    RETURN;
END_IF;

(* === SENSOR NOISE FILTERING & REDUNDANCY === *)
(* Calculate average between redundant ambient sensors. Trap deviations. *)
IF ABS(rAirTempSensor1 - rAirTempSensor2) > 15.0 THEN
    (* Deviation alarm if sensors mismatch by more than 15 degrees *)
    iCycleState := 99;
ELSE
    (* Apply a first-order low pass filter to the average for smooth control *)
    rAvgAirTemp := rAvgAirTemp + 0.1 * (((rAirTempSensor1 + rAirTempSensor2) / 2.0) - rAvgAirTemp);
END_IF;

(* === MAIN CURE CYCLE STATE MACHINE === *)
CASE iCycleState OF
    0: (* IDLE & READY *)
        bCriticalFault := FALSE;
        bCycleComplete := FALSE;
        bHeaterContactor := FALSE;
        rHeaterPowerCmd := 0.0;
        rPressureValveCmd := 0.0;
        rExhaustValveCmd := 0.0;
        bCoolingFan := FALSE;
        
        IF bEnableSequence THEN
            iCycleState := 10; (* Start pressurization *)
        END_IF;

    10: (* PRESSURIZATION PHASE *)
        (* Apply PI control to internal pressure *)
        rPressError := rTargetDwellPressure - rVesselPressure;
        rPressIntegral := rPressIntegral + rPressError;
        
        (* Anti-windup limit for integral term *)
        IF rPressIntegral > 1000.0 THEN rPressIntegral := 1000.0; END_IF;
        IF rPressIntegral < 0.0 THEN rPressIntegral := 0.0; END_IF;
        
        rPressureValveCmd := (Kp_Press * rPressError) + (Ki_Press * rPressIntegral);
        
        (* Saturate outputs to physical valve limits *)
        IF rPressureValveCmd > 100.0 THEN rPressureValveCmd := 100.0; END_IF;
        IF rPressureValveCmd < 0.0 THEN rPressureValveCmd := 0.0; END_IF;
        
        (* Wait until pressure is within 0.2 Bar of target before heating *)
        IF rVesselPressure >= (rTargetDwellPressure - 0.2) THEN
            iCycleState := 20; (* Proceed to heat-up once pressurized *)
        END_IF;

    20: (* HEAT-UP RAMP PHASE *)
        (* Cascade control strategy: Air temp drives part temp *)
        bHeaterContactor := TRUE;
        
        rTempError := rTargetDwellTemp - rPartTempSensor;
        rTempIntegral := rTempIntegral + rTempError;
        
        IF rTempIntegral > 5000.0 THEN rTempIntegral := 5000.0; END_IF;
        IF rTempIntegral < 0.0 THEN rTempIntegral := 0.0; END_IF;
        
        rHeaterPowerCmd := (Kp_Temp * rTempError) + (Ki_Temp * rTempIntegral);
        
        IF rHeaterPowerCmd > 100.0 THEN rHeaterPowerCmd := 100.0; END_IF;
        IF rHeaterPowerCmd < 0.0 THEN rHeaterPowerCmd := 0.0; END_IF;
        
        (* Maintain pressure continuously during thermal expansion *)
        rPressError := rTargetDwellPressure - rVesselPressure;
        rPressureValveCmd := (Kp_Press * rPressError); 
        IF rPressureValveCmd > 100.0 THEN rPressureValveCmd := 100.0; END_IF;
        IF rPressureValveCmd < 0.0 THEN rPressureValveCmd := 0.0; END_IF;

        IF rPartTempSensor >= (rTargetDwellTemp - 2.0) THEN
            iCycleState := 30; (* Proceed to curing dwell phase *)
        END_IF;

    30: (* DWELL / CURING PHASE *)
        (* Maintain precision Temperature and Pressure for prepreg cross-linking *)
        tDwellTimer(IN := TRUE, PT := T#120M); (* 120 minutes standard cure *)
        
        (* Heater PID (switched to air temp for fine regulation around target) *)
        rTempError := rTargetDwellTemp - rAvgAirTemp; 
        rHeaterPowerCmd := (Kp_Temp * rTempError);
        IF rHeaterPowerCmd > 100.0 THEN rHeaterPowerCmd := 100.0; END_IF;
        IF rHeaterPowerCmd < 0.0 THEN rHeaterPowerCmd := 0.0; END_IF;
        
        IF tDwellTimer.Q THEN
            tDwellTimer(IN := FALSE);
            iCycleState := 40;
        END_IF;

    40: (* COOL-DOWN PHASE *)
        (* Turn off heaters, engage circulation fans *)
        bHeaterContactor := FALSE;
        rHeaterPowerCmd := 0.0;
        bCoolingFan := TRUE;
        
        (* Wait for part surface temperature to reach safe handling limit *)
        IF rPartTempSensor < 50.0 THEN
            iCycleState := 50;
        END_IF;
        
    50: (* DEPRESSURIZATION *)
        bCoolingFan := FALSE;
        rPressureValveCmd := 0.0;
        rExhaustValveCmd := 20.0; (* Controlled, slow venting to prevent shock *)
        
        IF rVesselPressure < 0.1 THEN
            rExhaustValveCmd := 0.0;
            bCycleComplete := TRUE;
            iCycleState := 0; (* Reset sequence *)
        END_IF;

    99: (* FAULT ABORT STATE *)
        bCriticalFault := TRUE;
        bHeaterContactor := FALSE;
        rHeaterPowerCmd := 0.0;
        bCoolingFan := TRUE; (* Keep fan on to mitigate localized hot spots *)
        rPressureValveCmd := 0.0;
        rExhaustValveCmd := 100.0; (* Rapid depressurization for safety *)
        
        (* Require manual toggle of Master Enable to clear fault state *)
        IF NOT bEnableSequence THEN
            iCycleState := 0; 
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
