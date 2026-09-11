import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Advanced Superconducting Magnetic Energy Storage (SMES)**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Niobium-titanium coil 4.2K helium bath thermal stabilization, mega-ampere bidirectional DC-DC chopper modulation, and grid-tie sub-cycle fault ride-through injection). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_SMES_EnergyStorage\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Advanced Superconducting Magnetic Energy Storage (SMES)

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_SMES_CryoGridTieCtrl
VAR_INPUT
    bEnable             : BOOL;  (* System enable / start sequence *)
    bGridFault          : BOOL;  (* Grid fault detected (sub-cycle transient) *)
    bEmergencyStop      : BOOL;  (* Safety relay OK signal (active high) *)
    rCoilTemp_K         : REAL;  (* Niobium-titanium coil temperature in Kelvin *)
    rCoilCurrent_kA     : REAL;  (* Superconducting coil current in Kilo-Amperes *)
    rGridVoltage_kV     : REAL;  (* Instantaneous Grid Voltage in Kilo-Volts *)
    rRequestedPower_MW  : REAL;  (* Power requested for grid injection in Mega-Watts *)
END_VAR
VAR_OUTPUT
    bSystemReady        : BOOL;  (* System operational and at cryogenic standby *)
    rChopperDutyCycle   : REAL;  (* PWM Duty Cycle for Mega-Ampere DC-DC Chopper (0.0 - 100.0%) *)
    bGridInjectMode     : BOOL;  (* Active when discharging into the grid *)
    rHeliumFlow_Lpm     : REAL;  (* Liquid Helium flow rate in Liters per minute for thermal stabilization *)
    bQuenchAlarm        : BOOL;  (* Coil Quench Critical Alarm *)
    bAlarm              : BOOL;  (* General Warning / Fault Alarm *)
END_VAR
VAR
    iState              : INT := 0; 
    tCoolDownTimer      : TON;
    tGridFaultTimer     : TON;
    rTargetTemp_K       : REAL := 4.2; (* Nominal LHe temp *)
    rQuenchThreshold_K  : REAL := 5.5; (* Critical temp before quenching NbTi *)
    rTempError          : REAL;
    rKp_Cryo            : REAL := 15.0;
    rKi_Cryo            : REAL := 2.5;
    rIntegralCryo       : REAL := 0.0;
END_VAR

(* === MAIN LOGIC === *)
(* Safety Interlock Check *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bGridInjectMode := FALSE;
    rChopperDutyCycle := 0.0;
    bAlarm := TRUE;
    iState := 999; (* FAULT STATE *)
    RETURN;
END_IF;

(* Quench Protection - Highest Priority *)
IF rCoilTemp_K >= rQuenchThreshold_K THEN
    bQuenchAlarm := TRUE;
    bSystemReady := FALSE;
    bGridInjectMode := FALSE;
    rChopperDutyCycle := 0.0;
    rHeliumFlow_Lpm := 1000.0; (* Maximum emergency flush *)
    iState := 999;
    RETURN;
ELSE
    bQuenchAlarm := FALSE;
END_IF;

(* Cryogenic PID Control (Continuous background task) *)
rTempError := rCoilTemp_K - rTargetTemp_K;
IF rTempError > 0.0 THEN
    rIntegralCryo := rIntegralCryo + (rTempError * 0.1); (* Assuming 100ms cycle time *)
    IF rIntegralCryo > 500.0 THEN rIntegralCryo := 500.0; END_IF; (* Anti-windup *)
    rHeliumFlow_Lpm := (rKp_Cryo * rTempError) + (rKi_Cryo * rIntegralCryo);
ELSE
    rHeliumFlow_Lpm := 10.0; (* Minimum maintenance flow *)
    rIntegralCryo := 0.0;
END_IF;

(* State Machine for SMES Operational Modes *)
CASE iState OF
    0: (* IDLE *)
        bSystemReady := FALSE;
        bGridInjectMode := FALSE;
        rChopperDutyCycle := 0.0;
        IF bEnable AND (rCoilTemp_K <= 4.5) THEN
            iState := 10;
        ELSIF bEnable THEN
            iState := 5; (* Go to Cooldown *)
        END_IF;

    5: (* COOLING *)
        tCoolDownTimer(IN := TRUE, PT := T#60S);
        IF rCoilTemp_K <= 4.3 THEN
            tCoolDownTimer(IN := FALSE);
            iState := 10;
        ELSIF tCoolDownTimer.Q THEN
            (* Cool down timeout *)
            bAlarm := TRUE;
            tCoolDownTimer(IN := FALSE);
            iState := 0;
        END_IF;

    10: (* STANDBY & CHARGED *)
        bSystemReady := TRUE;
        rChopperDutyCycle := 50.0; (* Neutral duty for keeping current circulating (freewheeling) *)
        
        IF bGridFault THEN
            iState := 20; (* Fast transition to Grid Ride-Through *)
        ELSIF NOT bEnable THEN
            iState := 0;
        END_IF;

    20: (* GRID FAULT RIDE-THROUGH / INJECTION *)
        bGridInjectMode := TRUE;
        tGridFaultTimer(IN := TRUE, PT := T#2S); (* Max 2 seconds injection to prevent deep depletion *)
        
        (* Calculate required Chopper Duty Cycle to inject requested power based on current Coil energy *)
        IF rCoilCurrent_kA > 1.0 THEN
            (* P = V * I -> Modulation index adjustment *)
            rChopperDutyCycle := 50.0 + (rRequestedPower_MW / (rCoilCurrent_kA * rGridVoltage_kV)) * 50.0;
            IF rChopperDutyCycle > 95.0 THEN rChopperDutyCycle := 95.0; END_IF;
        ELSE
            rChopperDutyCycle := 50.0; (* Coil depleted *)
            iState := 10;
        END_IF;

        IF NOT bGridFault OR tGridFaultTimer.Q THEN
            tGridFaultTimer(IN := FALSE);
            bGridInjectMode := FALSE;
            iState := 10;
        END_IF;

    999: (* FAULT LOCKOUT *)
        IF bEmergencyStop AND NOT bQuenchAlarm AND NOT bEnable THEN
            bAlarm := FALSE;
            iState := 0;
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
