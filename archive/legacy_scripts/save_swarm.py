import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial Scale Green Ammonia Haber-Bosch Synthesis Loop**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 250-bar multipass catalytic reactor quenching, syngas H2:N2 ratio stoichiometry trimming, and continuous high-pressure separator purging). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_GreenAmmonia_HaberBosch\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Scale Green Ammonia Haber-Bosch Synthesis Loop

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_GreenAmmonia_HaberBosch
VAR_INPUT
    (* Required inputs for Haber-Bosch reactor control *)
    bEnable                 : BOOL;     (* System master enable for Synthesis Loop *)
    bEmergencyStop          : BOOL;     (* Safety instrumented system (SIS) trip signal, normally TRUE *)
    rH2N2RatioActual        : REAL;     (* Current H2:N2 stoichiometric ratio from gas chromatograph *)
    rReactorTemp            : REAL;     (* Catalyst bed temperature [deg C] *)
    rReactorPressure        : REAL;     (* Reactor operating pressure [bar] *)
    rSyngasFlowIn           : REAL;     (* Inlet syngas flow rate [kg/h] *)
    bQuenchValveOK          : BOOL;     (* Feedback from cold quench gas injection valve *)
    rPurgeGasFlow           : REAL;     (* High-pressure separator purge flow [Nm3/h] *)
END_VAR
VAR_OUTPUT
    (* Required outputs for actuation and safety *)
    bSystemReady            : BOOL;     (* Synthesis loop is pressurized, heated, and ready *)
    rQuenchValveCmd         : REAL;     (* Control signal to quench gas valve [0-100%] *)
    rPurgeValveCmd          : REAL;     (* Control signal to purge flow control valve [0-100%] *)
    bRatioTrimActive        : BOOL;     (* Indication that stoichiometric trimming is active *)
    bAlarm                  : BOOL;     (* General fault or deviation alarm *)
    bTripInitiated          : BOOL;     (* Safety trip triggered by this FB *)
END_VAR
VAR
    (* Internal State and PID Variables *)
    iState                  : INT := 0; (* State machine step index *)
    tStartupTimer           : TON;      (* Timer for reactor heating/pressurization *)
    rFilteredTemp           : REAL;     (* EMA filtered reactor temperature *)
    rFilteredPress          : REAL;     (* EMA filtered reactor pressure *)
    rTempError              : REAL;     (* Temperature deviation from setpoint *)
    rPressError             : REAL;     (* Pressure deviation from setpoint *)
    rTempSetpoint           : REAL := 450.0; (* Optimal catalyst temperature [deg C] *)
    rPressSetpoint          : REAL := 250.0; (* Optimal synthesis pressure [bar] *)
    
    (* Filter Constants *)
    rAlphaTemp              : REAL := 0.05;  (* EMA smoothing factor for temperature *)
    rAlphaPress             : REAL := 0.10;  (* EMA smoothing factor for pressure *)
    
    (* PID internal memory for Quench Valve (Temperature Control) *)
    rKp_Temp                : REAL := 2.5;
    rKi_Temp                : REAL := 0.01;
    rKd_Temp                : REAL := 0.5;
    rIntegral_Temp          : REAL := 0.0;
    rPrevError_Temp         : REAL := 0.0;
END_VAR

(* === MAIN LOGIC === *)
(* 1. Multi-layered Safety Interlocks and Hardware Checks *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    rQuenchValveCmd := 100.0; (* Fail-safe: full quench to stop runaway *)
    rPurgeValveCmd := 0.0;    (* Fail-safe: close purge to contain inventory *)
    bAlarm := TRUE;
    bTripInitiated := TRUE;
    iState := 99; (* Fault state *)
    RETURN;
END_IF;

(* 2. Sensor Noise Filtering (Exponential Moving Average) *)
rFilteredTemp := rFilteredTemp + rAlphaTemp * (rReactorTemp - rFilteredTemp);
rFilteredPress := rFilteredPress + rAlphaPress * (rReactorPressure - rFilteredPress);

(* 3. Hard Trip Limits for Protection *)
IF rFilteredTemp > 520.0 OR rFilteredPress > 280.0 THEN
    bTripInitiated := TRUE;
    bAlarm := TRUE;
    iState := 99;
END_IF;

(* 4. State Machine for Synthesis Loop Operation *)
CASE iState OF
    0: (* IDLE / INITIALIZATION *)
        bSystemReady := FALSE;
        bTripInitiated := FALSE;
        rQuenchValveCmd := 0.0;
        rPurgeValveCmd := 0.0;
        bRatioTrimActive := FALSE;
        IF bEnable THEN
            iState := 10;
        END_IF;
        
    10: (* PRESSURIZATION AND HEATING *)
        (* Wait for pressure and temperature to reach minimum operating conditions *)
        IF rFilteredTemp > 350.0 AND rFilteredPress > 200.0 THEN
            tStartupTimer(IN := TRUE, PT := T#30S);
            IF tStartupTimer.Q THEN
                tStartupTimer(IN := FALSE);
                iState := 20;
            END_IF;
        ELSE
            tStartupTimer(IN := FALSE);
        END_IF;
        IF NOT bEnable THEN
            iState := 0;
        END_IF;
        
    20: (* RUNNING - ACTIVE CONTROL *)
        bSystemReady := TRUE;
        
        (* Advanced PID Control for Quench Valve (Temperature) *)
        rTempError := rFilteredTemp - rTempSetpoint;
        rIntegral_Temp := rIntegral_Temp + rTempError;
        
        (* Anti-windup *)
        IF rIntegral_Temp > 1000.0 THEN rIntegral_Temp := 1000.0; END_IF;
        IF rIntegral_Temp < -1000.0 THEN rIntegral_Temp := -1000.0; END_IF;
        
        rQuenchValveCmd := (rKp_Temp * rTempError) + 
                           (rKi_Temp * rIntegral_Temp) + 
                           (rKd_Temp * (rTempError - rPrevError_Temp));
                           
        rPrevError_Temp := rTempError;
        
        (* Clamp Output *)
        IF rQuenchValveCmd > 100.0 THEN rQuenchValveCmd := 100.0; END_IF;
        IF rQuenchValveCmd < 0.0 THEN rQuenchValveCmd := 0.0; END_IF;
        
        (* Stoichiometry Trimming Logic *)
        IF rH2N2RatioActual > 3.1 OR rH2N2RatioActual < 2.9 THEN
            bRatioTrimActive := TRUE;
        ELSE
            bRatioTrimActive := FALSE;
        END_IF;
        
        (* Continuous High-Pressure Separator Purging based on inert buildup *)
        rPressError := rFilteredPress - rPressSetpoint;
        IF rPressError > 5.0 THEN
            rPurgeValveCmd := 15.0; (* 15% opening to vent inerts *)
        ELSE
            rPurgeValveCmd := 5.0;  (* Baseline purge *)
        END_IF;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;
        
    99: (* FAULT STATE *)
        bSystemReady := FALSE;
        rQuenchValveCmd := 100.0; (* Full quench *)
        rPurgeValveCmd := 0.0;
        IF NOT bEmergencyStop AND bEnable = FALSE THEN
            (* Require enable toggle to reset from fault if e-stop is cleared *)
            bAlarm := FALSE;
            iState := 0;
        END_IF;
END_CASE;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
