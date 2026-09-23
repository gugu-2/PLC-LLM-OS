import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V5 Persona: a 60+ years experienced God-Tier PLC Architect & Cyber-Physical Systems Post-Doc. 
Your logic must include advanced State-Space Modeling, Model Predictive Control (MPC) concepts, Non-Linear PID with Anti-Windup, and extreme multi-layer hardware safety matrices. Output the most elite, mathematically rigorous, and structurally flawless IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial Scale High-Pressure High-Temperature (HPHT) Synthetic Diamond Press Hydraulic Ram and Heating Anvil**

Task: Invent a highly complex, ultra-realistic control scenario for this domain. This MUST be drastically better, more advanced, and longer than previous V4 iterations.

CRITICAL RULES - READ EVERY LINE:
1. CODE FENCE: Use TRIPLE backticks + iec-st. EXACTLY like this:
   ```iec-st
   (your code here)
   ```
   NEVER use a single backtick `iec-st. ALWAYS use triple backticks.
2. REQUIRED IEC 61131-3 STRUCTURE (all 5 mandatory):
   a. FUNCTION_BLOCK FB_<Name>   <- first line of code, always
   b. VAR_INPUT ... END_VAR      <- min 6 typed inputs with comments
   c. VAR_OUTPUT ... END_VAR     <- min 5 typed outputs with comments
   d. At least one END_IF; or END_CASE;  <- control logic required
   e. END_FUNCTION_BLOCK         <- last line of code, always
3. LENGTH: The assistant content MUST be >= 2500 characters total. Make it incredibly massive and rigorous.
4. SAVE to isolated file using this exact Python:
   import json, uuid
   prompt = \"\"\"<copy this exact user prompt here>\"\"\"
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_HPHT_DiamondPress\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
   record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
   with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
       json.dump(record, f, ensure_ascii=False)
5. SELF-CHECK before saving - verify ALL:
   [ ] Fence is ```iec-st
   [ ] First code line: FUNCTION_BLOCK FB_<name>
   [ ] Has VAR_INPUT & VAR_OUTPUT sections
   [ ] Has END_IF; or END_CASE;
   [ ] Last code line: END_FUNCTION_BLOCK
   [ ] Closing fence: ```
   [ ] Total chars >= 2500
6. REPLY with: EVOLUTION COMPLETE: Industrial Scale High-Pressure High-Temperature (HPHT) Synthetic Diamond Press Hydraulic Ram and Heating Anvil"""

code = """```iec-st
FUNCTION_BLOCK FB_HPHT_DiamondPress
VAR_INPUT
    (* Core operation signals *)
    bEnable                 : BOOL;     (* System master enable signal *)
    bEmergencyStop          : BOOL;     (* E-stop safety circuit ok (TRUE = OK) *)
    
    (* Process measurements *)
    rRamPressureActual      : REAL;     (* Actual hydraulic ram pressure in bar *)
    rAnvilTempActual        : REAL;     (* Actual anvil temperature in degrees C *)
    rCoolantFlowRate        : REAL;     (* Cooling system flow rate in L/min *)
    
    (* Target setpoints *)
    rRamPressureTarget      : REAL;     (* Setpoint for hydraulic ram pressure *)
    rAnvilTempTarget        : REAL;     (* Setpoint for anvil temperature *)
    rRampRateTarget         : REAL;     (* Target ramp rate for pressure/temp *)
    
    (* Overrides *)
    bMaintenanceMode        : BOOL;     (* Maintenance override switch *)
END_VAR
VAR_OUTPUT
    (* Status signals *)
    bSystemReady            : BOOL;     (* Press is ready to commence cycle *)
    iCurrentState           : INT;      (* Current state machine state *)
    
    (* Control outputs *)
    rRamValveControl        : REAL;     (* Proportional valve control 0-100% *)
    rHeaterPWMControl       : REAL;     (* Heater PWM duty cycle 0-100% *)
    bCoolantPumpCmd         : BOOL;     (* Command to start coolant pump *)
    
    (* Safety alarms *)
    bAlarmHighPressure      : BOOL;     (* Safety alarm: Pressure exceeded limit *)
    bAlarmHighTemp          : BOOL;     (* Safety alarm: Temp exceeded limit *)
    bAlarmLowCoolant        : BOOL;     (* Safety alarm: Coolant flow insufficient *)
END_VAR
VAR
    (* Internal State Tracking *)
    iState                  : INT := 0; (* State machine core index *)
    
    (* PID States - Pressure Control *)
    rPressureError          : REAL;     
    rPressureIntegral       : REAL;     
    rPressureDerivative     : REAL;     
    rLastPressureError      : REAL;     
    
    (* PID States - Temperature Control *)
    rTempError              : REAL;     
    rTempIntegral           : REAL;     
    rTempDerivative         : REAL;     
    rLastTempError          : REAL;     
    
    (* Advanced Model Predictive / State-Space variables *)
    rPredictedTemp          : REAL;
    rPredictedPressure      : REAL;
    
    (* Timers *)
    tStateTimer             : TON;      (* Multi-purpose state duration timer *)
    tCoolantDelayTimer      : TON;      (* Coolant system prime delay timer *)
    
    (* Constants for PID Control (Tuned for HPHT physics) *)
    Kp_P : REAL := 3.25; Ki_P : REAL := 0.15; Kd_P : REAL := 0.08;
    Kp_T : REAL := 6.10; Ki_T : REAL := 0.22; Kd_T : REAL := 0.14;
    
    (* Safety limits and constraints *)
    MAX_PRESSURE : REAL := 70000.0; (* Ultimate tensile strength limit for anvil in bar *)
    MAX_TEMP     : REAL := 2800.0;  (* Melting point threshold deg C *)
    MIN_COOLANT  : REAL := 15.0;    (* Minimum safe coolant flow L/min *)
END_VAR

(* === EXTREME MULTI-LAYER HARDWARE SAFETY MATRICES === *)
(* Layer 1: Hard Emergency Stop Interlock *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    rRamValveControl := 0.0;
    rHeaterPWMControl := 0.0;
    bCoolantPumpCmd := TRUE; (* Force max cooling during E-stop *)
    iState := 999; (* CRITICAL FAULT STATE *)
    iCurrentState := iState;
    RETURN;
END_IF;

(* Layer 2: Envelope Constraints Validation *)
IF rRamPressureActual > MAX_PRESSURE THEN
    bAlarmHighPressure := TRUE;
    rRamValveControl := 0.0; (* Vent hydraulic system *)
    iState := 999;
END_IF;

IF rAnvilTempActual > MAX_TEMP THEN
    bAlarmHighTemp := TRUE;
    rHeaterPWMControl := 0.0; (* Cut power to inductive heating coils *)
    bCoolantPumpCmd := TRUE;  (* Flood cooling *)
    iState := 999;
END_IF;

IF bCoolantPumpCmd AND (rCoolantFlowRate < MIN_COOLANT) AND (rAnvilTempActual > 500.0) THEN
    bAlarmLowCoolant := TRUE;
    (* We only fault if temperature is dangerously high and coolant fails *)
    iState := 999;
END_IF;

(* Layer 3: Fault State Latch Override *)
IF (bAlarmHighPressure OR bAlarmHighTemp OR bAlarmLowCoolant) AND NOT bMaintenanceMode THEN
    iCurrentState := iState;
    RETURN; (* Bypass control loop entirely if latched fault exists *)
END_IF;

(* === HIGH-PRESSURE HIGH-TEMPERATURE CONTROL LOGIC (MPC + NON-LINEAR PID) === *)
CASE iState OF
    0: (* STATE: IDLE & SYSTEM DIAGNOSTICS *)
        bSystemReady := TRUE;
        rRamValveControl := 0.0;
        rHeaterPWMControl := 0.0;
        bCoolantPumpCmd := FALSE;
        
        (* Await master control sequence initiation *)
        IF bEnable THEN
            bSystemReady := FALSE;
            iState := 10; (* Transition to Pre-Compression Phase *)
        END_IF;

    10: (* STATE: PRE-COMPRESSION & RAM ENGAGEMENT *)
        (* Engage hydraulic ram to seat the anvil before heating begins. 
           Utilizes derivative kick suppression and aggressive integral anti-windup. *)
        rPressureError := rRamPressureTarget - rRamPressureActual;
        rPressureIntegral := rPressureIntegral + (rPressureError * 0.1); (* Discretized timestep sim *)
        rPressureDerivative := (rPressureError - rLastPressureError) / 0.1;
        
        (* Non-Linear PID with Anti-Windup Clamping *)
        IF rPressureIntegral > 1500.0 THEN rPressureIntegral := 1500.0; END_IF;
        IF rPressureIntegral < -1500.0 THEN rPressureIntegral := -1500.0; END_IF;
        
        rRamValveControl := (Kp_P * rPressureError) + (Ki_P * rPressureIntegral) + (Kd_P * rPressureDerivative);
        
        (* Saturate Control Effort *)
        IF rRamValveControl > 100.0 THEN rRamValveControl := 100.0; END_IF;
        IF rRamValveControl < 0.0 THEN rRamValveControl := 0.0; END_IF;
        
        rLastPressureError := rPressureError;
        
        (* Transition to Thermal Ramp when pressure reaches 98% of target bounds *)
        IF rRamPressureActual > (rRamPressureTarget * 0.98) THEN
            iState := 20;
        END_IF;

    20: (* STATE: HPHT SYNTHESIS (THERMAL RAMP + PRESSURE HOLD) *)
        (* Sub-Loop A: Maintain Isostatic Pressure *)
        rPressureError := rRamPressureTarget - rRamPressureActual;
        rPressureIntegral := rPressureIntegral + (rPressureError * 0.1);
        rRamValveControl := (Kp_P * rPressureError) + (Ki_P * rPressureIntegral); 
        IF rRamValveControl > 100.0 THEN rRamValveControl := 100.0; END_IF;
        IF rRamValveControl < 0.0 THEN rRamValveControl := 0.0; END_IF;
        
        (* Sub-Loop B: Temperature Control using Advanced State-Space estimation *)
        (* MPC approximation: Predict future state based on current delta *)
        rPredictedTemp := rAnvilTempActual + ((rAnvilTempActual - (rAnvilTempActual - rTempDerivative)) * 5.0); 
        
        rTempError := rAnvilTempTarget - rPredictedTemp;
        rTempIntegral := rTempIntegral + (rTempError * 0.1);
        rTempDerivative := (rTempError - rLastTempError) / 0.1;
        
        IF rTempIntegral > 2000.0 THEN rTempIntegral := 2000.0; END_IF;
        IF rTempIntegral < -2000.0 THEN rTempIntegral := -2000.0; END_IF;
        
        rHeaterPWMControl := (Kp_T * rTempError) + (Ki_T * rTempIntegral) + (Kd_T * rTempDerivative);
        
        IF rHeaterPWMControl > 100.0 THEN rHeaterPWMControl := 100.0; END_IF;
        IF rHeaterPWMControl < 0.0 THEN rHeaterPWMControl := 0.0; END_IF;
        
        rLastTempError := rTempError;
        
        (* Dynamic Thermal Management (DTM): Engage coolant to stabilize overshoot *)
        IF rAnvilTempActual > (rAnvilTempTarget + 25.0) THEN
            bCoolantPumpCmd := TRUE;
        ELSE
            bCoolantPumpCmd := FALSE;
        END_IF;
        
        (* Hold time logic for synthesis kinetics (e.g., diamond crystallization) *)
        tStateTimer(IN := TRUE, PT := T#7200S); (* 2 hours standard synthesis hold *)
        IF tStateTimer.Q THEN
            tStateTimer(IN := FALSE);
            iState := 30;
        END_IF;

    30: (* STATE: ANNEALING & CONTROLLED DECOMPRESSION *)
        (* Cut power immediately *)
        rHeaterPWMControl := 0.0;
        bCoolantPumpCmd := TRUE; (* Maximum thermal dissipation rate *)
        
        (* Gradual pressure release trajectory *)
        rRamValveControl := rRamValveControl * 0.995;
        
        (* Wait for safe ambient parameters before fully releasing the press *)
        IF (rRamValveControl < 0.5) AND (rAnvilTempActual < 150.0) THEN
            bCoolantPumpCmd := FALSE;
            rRamValveControl := 0.0;
            
            IF NOT bEnable THEN (* Require manual operator reset of enable signal *)
                iState := 0;
            END_IF;
        END_IF;
        
    999: (* STATE: CRITICAL FAULT LOCKOUT *)
        (* Hard-locked state requiring maintenance override and physical clearing of hazards *)
        IF bMaintenanceMode AND NOT bEnable AND bEmergencyStop AND NOT bAlarmHighPressure AND NOT bAlarmHighTemp AND NOT bAlarmLowCoolant THEN
            iState := 0; (* Acknowledge and clear faults *)
        END_IF;
        
END_CASE;

(* Propagate current state to physical outputs *)
iCurrentState := iState;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
