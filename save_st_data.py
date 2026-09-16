import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Cryogenic Distillation Column for Air Separation (Liquid Oxygen/Nitrogen)**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Expansion turbine Joule-Thomson cooling regulation, tray temperature profile stabilization, and argon side-draw purity optimization). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Cryo_AirSeparation\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Cryogenic Distillation Column for Air Separation (Liquid Oxygen/Nitrogen)

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_CryoDistillation_AirSep
VAR_INPUT
    (* Physical Inputs *)
    bEnable                 : BOOL;     (* System enable command from main SCADA *)
    bEmergencyStop          : BOOL;     (* Main plant emergency stop, safety loop active low *)
    rFeedFlowRate           : REAL;     (* Pre-purified air feed mass flow rate [kg/h] *)
    rFeedTemp               : REAL;     (* Pre-purified air feed temperature [K] *)
    rTopPressure            : REAL;     (* Column top pressure [bar] *)
    rBottomTemp             : REAL;     (* Column bottom reboiler temperature [K] *)
    rArgonDrawFlow          : REAL;     (* Side draw argon mass flow rate [kg/h] *)
    rTurbineSpeed           : REAL;     (* Expansion turbine speed [RPM] *)
END_VAR
VAR_OUTPUT
    (* Physical Outputs *)
    bSystemReady            : BOOL;     (* System healthy and running nominal *)
    rNitrogenRefluxValve    : REAL;     (* Valve position for LN2 reflux [0-100%] *)
    rOxygenProductValve     : REAL;     (* Valve position for LOX product extraction [0-100%] *)
    rTurbineGuideVane       : REAL;     (* Guide vane position for turbine cooling [0-100%] *)
    bHighPressureAlarm      : BOOL;     (* Alarm indicating overpressure at top *)
    bTemperatureFault       : BOOL;     (* Bottom reboiler temp out of bounds *)
END_VAR
VAR
    (* Internal state and timers *)
    iState                  : INT := 0;
    tStabilizationTimer     : TON;
    tSafetyTimer            : TON;
    
    (* Filtered values and internal calculations *)
    rFilteredFeedFlow       : REAL := 0.0;
    rTopPressDeviation      : REAL;
    
    (* PID control states *)
    rN2RefluxIntegral       : REAL := 0.0;
    rO2ProductIntegral      : REAL := 0.0;
    rTurbineIntegral        : REAL := 0.0;
    
    (* Constants *)
    Kp_N2                   : REAL := 2.5;
    Ki_N2                   : REAL := 0.1;
    Kp_O2                   : REAL := 1.8;
    Ki_O2                   : REAL := 0.05;
    Kp_Turb                 : REAL := 3.2;
    Ki_Turb                 : REAL := 0.15;
    
    PRESSURE_SETPOINT       : REAL := 5.8;  (* Nominal operating pressure in bar *)
    TEMP_SETPOINT_BOT       : REAL := 90.1; (* Nominal LOX boiling point at operating pressure [K] *)
    TURBINE_SPEED_SET       : REAL := 45000.0; (* Optimal expansion turbine RPM *)
END_VAR

(* === MAIN LOGIC === *)
(* First-Pass Filtering of noise using simple EWMA filter (alpha = 0.1) *)
rFilteredFeedFlow := (rFeedFlowRate * 0.1) + (rFilteredFeedFlow * 0.9);

(* Safety Interlocks *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bHighPressureAlarm := FALSE;
    bTemperatureFault := FALSE;
    
    (* Fail-safe states for critical valves *)
    rNitrogenRefluxValve := 100.0; (* Full reflux to prevent loss of cooling *)
    rOxygenProductValve := 0.0;    (* Stop extraction *)
    rTurbineGuideVane := 0.0;      (* Minimum expansion *)
    
    iState := 0;
    RETURN;
END_IF;

(* Basic Alarms *)
bHighPressureAlarm := (rTopPressure > 6.2);
bTemperatureFault := (rBottomTemp < 88.0) OR (rBottomTemp > 93.0);

(* State Machine for Plant Startup and Operation *)
CASE iState OF
    0: (* IDLE *)
        bSystemReady := FALSE;
        rNitrogenRefluxValve := 100.0;
        rOxygenProductValve := 0.0;
        rTurbineGuideVane := 10.0; (* Slight bleed to keep turbine spinning *)
        
        IF bEnable AND NOT bHighPressureAlarm AND NOT bTemperatureFault THEN
            iState := 10;
        END_IF;

    10: (* PRE-COOLING AND PRESSURE BUILDUP *)
        (* Gradually open guide vanes to start cooling process *)
        rTurbineGuideVane := rTurbineGuideVane + 0.05;
        IF rTurbineGuideVane > 80.0 THEN
            rTurbineGuideVane := 80.0;
        END_IF;
        
        tStabilizationTimer(IN := TRUE, PT := T#30S);
        IF (rTopPressure >= 5.0) AND tStabilizationTimer.Q THEN
            tStabilizationTimer(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* PID ACTIVE / RUNNING *)
        bSystemReady := TRUE;
        
        (* 1. Nitrogen Reflux Control (Pressure control) *)
        rTopPressDeviation := PRESSURE_SETPOINT - rTopPressure;
        rN2RefluxIntegral := rN2RefluxIntegral + (rTopPressDeviation * Ki_N2);
        
        (* Anti-windup *)
        IF rN2RefluxIntegral > 50.0 THEN rN2RefluxIntegral := 50.0; END_IF;
        IF rN2RefluxIntegral < -50.0 THEN rN2RefluxIntegral := -50.0; END_IF;
        
        rNitrogenRefluxValve := 50.0 - (rTopPressDeviation * Kp_N2 + rN2RefluxIntegral);
        
        (* Saturate valve output *)
        IF rNitrogenRefluxValve > 100.0 THEN rNitrogenRefluxValve := 100.0; END_IF;
        IF rNitrogenRefluxValve < 10.0 THEN rNitrogenRefluxValve := 10.0; END_IF; (* Maintain min reflux *)

        (* 2. Oxygen Product Extraction (Bottom Temperature/Level control proxy) *)
        rO2ProductIntegral := rO2ProductIntegral + ((rBottomTemp - TEMP_SETPOINT_BOT) * Ki_O2);
        rOxygenProductValve := 30.0 + ((rBottomTemp - TEMP_SETPOINT_BOT) * Kp_O2 + rO2ProductIntegral);
        IF rOxygenProductValve > 100.0 THEN rOxygenProductValve := 100.0; END_IF;
        IF rOxygenProductValve < 0.0 THEN rOxygenProductValve := 0.0; END_IF;

        (* 3. Turbine Cooling Duty (Speed Control) *)
        rTurbineIntegral := rTurbineIntegral + ((TURBINE_SPEED_SET - rTurbineSpeed) * 0.0001 * Ki_Turb);
        rTurbineGuideVane := 50.0 + ((TURBINE_SPEED_SET - rTurbineSpeed) * 0.001 * Kp_Turb + rTurbineIntegral);
        IF rTurbineGuideVane > 100.0 THEN rTurbineGuideVane := 100.0; END_IF;
        IF rTurbineGuideVane < 5.0 THEN rTurbineGuideVane := 5.0; END_IF;
        
        (* Check exit condition *)
        IF NOT bEnable OR bHighPressureAlarm THEN
            iState := 30;
        END_IF;
        
    30: (* SHUTDOWN SEQUENCE *)
        bSystemReady := FALSE;
        rOxygenProductValve := 0.0;
        
        (* Slowly close guide vane and reflux to avoid hammer *)
        rTurbineGuideVane := rTurbineGuideVane - 0.5;
        IF rTurbineGuideVane < 0.0 THEN rTurbineGuideVane := 0.0; END_IF;
        
        rNitrogenRefluxValve := rNitrogenRefluxValve + 1.0;
        IF rNitrogenRefluxValve > 100.0 THEN rNitrogenRefluxValve := 100.0; END_IF;
        
        IF (rTurbineGuideVane <= 0.0) AND (rNitrogenRefluxValve >= 100.0) THEN
            iState := 0;
        END_IF;

END_CASE;

(* Ensure tStabilizationTimer is updated if state is not 10 *)
IF iState <> 10 THEN
    tStabilizationTimer(IN := FALSE);
END_IF;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
