import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial Scale High-Altitude Precision Stratospheric Airship Ballonet**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Diurnal solar thermal volume expansion compensation, superpressure multi-chamber envelope load distribution, and helium valving differential mass flow rate). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_StratosphericAirship_Ballonet\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Scale High-Altitude Precision Stratospheric Airship Ballonet

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_StratosphericAirship_Ballonet
(*
==================================================================================
 FB Name       : FB_StratosphericAirship_Ballonet
 Description   : Advanced control logic for stratospheric airship ballonet systems.
                 Handles diurnal solar thermal expansion, multi-chamber superpressure
                 distribution, and helium mass flow balancing.
 Author        : Lumina Elite Automation Architect
 Version       : 4.1.0
==================================================================================
*)

VAR_INPUT
    (* System Signals *)
    bEnable                 : BOOL;     (* Master system enable signal *)
    bEmergencyStop          : BOOL;     (* Safety relay OK / E-Stop signal (Active LOW for fault) *)
    
    (* Environment & State Sensors *)
    rAltitude_m             : REAL;     (* Current MSL altitude in meters *)
    rSolarIrradiance_Wm2    : REAL;     (* Solar irradiance (W/m^2) for thermal compensation *)
    rInternalTemp_K         : REAL;     (* Internal envelope temperature (Kelvin) *)
    rExternalTemp_K         : REAL;     (* Ambient atmospheric temperature (Kelvin) *)
    
    (* Pressure Sensors *)
    rHeliumPressure_Pa      : REAL;     (* Main lifting gas chamber pressure (Pascals) *)
    rBallonetPressure_Pa    : REAL;     (* Internal ballonet pressure (Pascals) *)
    
    (* Mechanical Feedback *)
    bBlowerFault            : BOOL;     (* Blower motor overcurrent or fault feedback *)
    bValvesStuck            : BOOL;     (* Limit switch feedback indicating valving failure *)
END_VAR

VAR_OUTPUT
    (* System Status *)
    bSystemReady            : BOOL;     (* System initialized and ready for flight profile *)
    bAlarm                  : BOOL;     (* Fault alarm output (Critical/Warning) *)
    iErrorCode              : INT;      (* Diagnostics error code *)
    
    (* Actuator Commands *)
    rBlowerSpeedCmd         : REAL;     (* 0.0 to 100.0% command to ballonet intake blowers *)
    rBallonetVentValvesCmd  : REAL;     (* 0.0 to 100.0% command to ballonet air exhaust valves *)
    bHeliumEmergencyVent    : BOOL;     (* Discrete trigger for helium emergency blow-off valves *)
    
    (* Telemetry *)
    rCalculatedDiffPress    : REAL;     (* Smoothed differential pressure telemetry *)
END_VAR

VAR
    (* Internal State & Timers *)
    iState                  : INT := 0; 
    tInitDelay              : TON;
    
    (* Advanced Filtering (EMA) *)
    rAlpha                  : REAL := 0.15; (* Smoothing factor *)
    rSmoothedHe_Pa          : REAL := 101325.0;
    rSmoothedBal_Pa         : REAL := 101325.0;
    
    (* Thermal Expansion & PID parameters *)
    rTargetDiffPress_Pa     : REAL := 250.0; (* 2.5 mBar nominal superpressure *)
    rMaxSuperpressure_Pa    : REAL := 800.0; (* Envelope burst limit threshold *)
    
    rKp                     : REAL := 0.25;
    rKi                     : REAL := 0.05;
    rError                  : REAL;
    rIntegral               : REAL := 0.0;
    
    bThermalCompActive      : BOOL := FALSE;
END_VAR

(* === SENSOR FILTERING & SAFETY INTERLOCKS === *)
(* Exponential Moving Average Filter for pressure sensors to reject atmospheric noise *)
rSmoothedHe_Pa := (rAlpha * rHeliumPressure_Pa) + ((1.0 - rAlpha) * rSmoothedHe_Pa);
rSmoothedBal_Pa := (rAlpha * rBallonetPressure_Pa) + ((1.0 - rAlpha) * rSmoothedBal_Pa);
rCalculatedDiffPress := rSmoothedHe_Pa - rSmoothedBal_Pa;

(* CRITICAL SAFETY: E-Stop and Hardware Faults bypass all logic *)
IF bEmergencyStop OR bBlowerFault OR bValvesStuck THEN
    bSystemReady := FALSE;
    bAlarm := TRUE;
    iErrorCode := 9999; (* 9999 = Critical Hardware Fault *)
    
    (* Fail-safe states for actuators *)
    rBlowerSpeedCmd := 0.0;
    rBallonetVentValvesCmd := 100.0; (* Fail open to prevent burst *)
    bHeliumEmergencyVent := FALSE;
    iState := 0;
    RETURN;
END_IF;

(* Check for critical envelope overpressure (independent of control loop) *)
IF rCalculatedDiffPress > rMaxSuperpressure_Pa THEN
    bHeliumEmergencyVent := TRUE;
    bAlarm := TRUE;
    iErrorCode := 8888; (* Envelope overpressure critical *)
ELSE
    bHeliumEmergencyVent := FALSE;
END_IF;

(* === MAIN CONTROL STATE MACHINE === *)
CASE iState OF
    0: (* IDLE & STANDBY *)
        bSystemReady := FALSE;
        bAlarm := FALSE;
        iErrorCode := 0;
        rBlowerSpeedCmd := 0.0;
        rBallonetVentValvesCmd := 0.0;
        
        IF bEnable THEN
            iState := 10;
        END_IF;

    10: (* INITIALIZING *)
        tInitDelay(IN := TRUE, PT := T#10S);
        rBallonetVentValvesCmd := 100.0; (* Purge sequence *)
        rBlowerSpeedCmd := 20.0;         (* Low speed test *)
        
        IF tInitDelay.Q THEN
            tInitDelay(IN := FALSE);
            bSystemReady := TRUE;
            iState := 20;
        END_IF;

    20: (* ACTIVE FLIGHT PROFILE - SUPERPRESSURE CONTROL *)
        (* Solar thermal compensation adjustment *)
        IF rSolarIrradiance_Wm2 > 400.0 AND rAltitude_m > 15000.0 THEN
            bThermalCompActive := TRUE;
            rTargetDiffPress_Pa := 300.0; (* Increase target during solar heating expansion *)
        ELSE
            bThermalCompActive := FALSE;
            rTargetDiffPress_Pa := 250.0;
        END_IF;

        (* PI Control for Ballonet volume management *)
        rError := rTargetDiffPress_Pa - rCalculatedDiffPress;
        rIntegral := rIntegral + (rError * 0.1); (* 100ms cycle assumption *)
        
        (* Anti-windup limit for integral *)
        IF rIntegral > 50.0 THEN rIntegral := 50.0; END_IF;
        IF rIntegral < -50.0 THEN rIntegral := -50.0; END_IF;
        
        (* If Error is positive, we need more pressure (inflate ballonet with air) *)
        IF rError > 0.0 THEN
            rBlowerSpeedCmd := (rError * rKp) + (rIntegral * rKi);
            rBallonetVentValvesCmd := 0.0;
            (* Saturate command *)
            IF rBlowerSpeedCmd > 100.0 THEN rBlowerSpeedCmd := 100.0; END_IF;
        ELSE
            (* If Error is negative, we have too much pressure (vent ballonet air) *)
            rBlowerSpeedCmd := 0.0;
            rBallonetVentValvesCmd := ABS(rError * rKp) + ABS(rIntegral * rKi);
            IF rBallonetVentValvesCmd > 100.0 THEN rBallonetVentValvesCmd := 100.0; END_IF;
        END_IF;

        (* State exit condition *)
        IF NOT bEnable THEN
            iState := 0;
        END_IF;
        
    ELSE
        (* CATCH-ALL *)
        iState := 0;
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
