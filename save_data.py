import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Utility-Scale Municipal Solid Waste (MSW) Plasma Gasification**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 10,000°C plasma torch power stabilization, syngas (CO/H2) real-time caloric value tracking, and vitreous slag taphole induction heating). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_PlasmaGasification\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Utility-Scale Municipal Solid Waste (MSW) Plasma Gasification

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_MSW_PlasmaGasification
(* ==============================================================================
   Title: FB_MSW_PlasmaGasification
   Description: Advanced deterministic control system for utility-scale Municipal 
                Solid Waste (MSW) plasma gasification. Implements non-linear PID 
                stabilization of 10,000°C plasma torch power, real-time tracking 
                of syngas (CO/H2) lower heating value (LHV), and induction 
                heating regulation for the continuous slag taphole.
   Author: Lumina Elite Automation Architect
   Date: 2026-09-06
   Version: 4.0.2 (High-Integrity Systems)
   ============================================================================== *)
VAR_INPUT
    (* Core Process Safety and Enable *)
    bSystemEnable       : BOOL;     (* Global process enable *)
    bEmergencyStop      : BOOL;     (* Safety relay loop status (FALSE = Trip) *)
    
    (* Plasma Torch Parameters *)
    rTorchVoltage_kV    : REAL;     (* Measured DC plasma torch voltage [kV] *)
    rTorchCurrent_kA    : REAL;     (* Measured DC plasma torch current [kA] *)
    
    (* Gasification Reactor Sensors *)
    rReactorTemp_C      : REAL;     (* Main reactor internal temperature [°C] *)
    rSyngasCO_Pct       : REAL;     (* Syngas Carbon Monoxide concentration [%] *)
    rSyngasH2_Pct       : REAL;     (* Syngas Hydrogen concentration [%] *)
    
    (* Slag Handling *)
    rSlagTemp_C         : REAL;     (* Vitreous slag temperature at taphole [°C] *)
END_VAR

VAR_OUTPUT
    (* Status and Safety *)
    bSystemReady        : BOOL;     (* TRUE when startup sequence is complete *)
    bCriticalAlarm      : BOOL;     (* TRUE on any out-of-bounds safety parameter *)
    iOperatingState     : INT;      (* Current state machine step *)

    (* Actuator Control Signals *)
    rTorchPowerDemand_MW: REAL;     (* Computed power setpoint for torch rectifier [MW] *)
    rSyngasLHV_MJ_Nm3   : REAL;     (* Calculated Lower Heating Value of Syngas [MJ/Nm3] *)
    rTapholeHeaterCmd   : REAL;     (* Slag induction heater PWM command [0.0 - 100.0 %] *)
END_VAR

VAR
    (* Internal State Machine and Timers *)
    iState              : INT := 0; 
    tPurgeTimer         : TON;
    tPreheatTimer       : TON;
    tStabilizationTimer : TON;
    
    (* Internal Computations *)
    rActualTorchPower   : REAL;     (* Calculated real-time power [MW] *)
    rPowerError         : REAL;     (* Torch power PID error [MW] *)
    rIntegralTerm       : REAL := 0.0;
    
    (* Constants *)
    c_Kp                : REAL := 1.25;
    c_Ki                : REAL := 0.05;
    c_MaxPower_MW       : REAL := 25.0;  (* 25 MW max per torch *)
    c_MinSlagTemp       : REAL := 1450.0;(* Minimum viscosity temperature for taphole [°C] *)
END_VAR

(* === MAIN LOGIC === *)

(* Safety Interlock Block *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bCriticalAlarm := TRUE;
    rTorchPowerDemand_MW := 0.0;
    rTapholeHeaterCmd := 0.0;
    iState := 999; (* FAULT STATE *)
    RETURN;
END_IF;

(* Compute Current Operating Metrics *)
rActualTorchPower := rTorchVoltage_kV * rTorchCurrent_kA;

(* Calculate Syngas Lower Heating Value (Empirical approximation based on CO/H2)
   1 Nm3 CO ~ 12.63 MJ, 1 Nm3 H2 ~ 10.78 MJ *)
rSyngasLHV_MJ_Nm3 := (rSyngasCO_Pct / 100.0 * 12.63) + (rSyngasH2_Pct / 100.0 * 10.78);

(* Taphole Induction Heater PI Control (Simplified) 
   Maintains slag in vitreous molten state (>1450C) *)
IF rSlagTemp_C < c_MinSlagTemp THEN
    rTapholeHeaterCmd := rTapholeHeaterCmd + 0.5; (* Increase heat *)
ELSE
    rTapholeHeaterCmd := rTapholeHeaterCmd - 0.2; (* Decrease heat slowly *)
END_IF;

(* Bound Heater Output *)
IF rTapholeHeaterCmd > 100.0 THEN
    rTapholeHeaterCmd := 100.0;
ELSIF rTapholeHeaterCmd < 0.0 THEN
    rTapholeHeaterCmd := 0.0;
END_IF;

(* Main State Machine *)
CASE iState OF
    0: (* IDLE & SYSTEM CHECK *)
        bSystemReady := FALSE;
        bCriticalAlarm := FALSE;
        rTorchPowerDemand_MW := 0.0;
        
        IF bSystemEnable THEN
            iState := 10;
        END_IF;

    10: (* INERT GAS PURGE *)
        tPurgeTimer(IN := TRUE, PT := T#30S);
        IF tPurgeTimer.Q THEN
            tPurgeTimer(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* PLASMA PREHEAT & ARC IGNITION *)
        rTorchPowerDemand_MW := 2.5; (* Ignition setpoint *)
        tPreheatTimer(IN := TRUE, PT := T#15S);
        
        IF tPreheatTimer.Q AND (rActualTorchPower > 1.0) THEN
            tPreheatTimer(IN := FALSE);
            iState := 30;
        ELSIF tPreheatTimer.Q THEN
            (* Arc failure *)
            bCriticalAlarm := TRUE;
            iState := 0;
        END_IF;

    30: (* RAMP & STABILIZATION (RUNNING) *)
        bSystemReady := TRUE;
        
        (* PI Power Control Loop for 15MW Target *)
        rPowerError := 15.0 - rActualTorchPower;
        rIntegralTerm := rIntegralTerm + (rPowerError * c_Ki);
        
        (* Anti-windup *)
        IF rIntegralTerm > c_MaxPower_MW THEN
            rIntegralTerm := c_MaxPower_MW;
        ELSIF rIntegralTerm < 0.0 THEN
            rIntegralTerm := 0.0;
        END_IF;
        
        rTorchPowerDemand_MW := (rPowerError * c_Kp) + rIntegralTerm;
        
        (* Limit Output *)
        IF rTorchPowerDemand_MW > c_MaxPower_MW THEN
            rTorchPowerDemand_MW := c_MaxPower_MW;
        ELSIF rTorchPowerDemand_MW < 0.0 THEN
            rTorchPowerDemand_MW := 0.0;
        END_IF;
        
        (* Check graceful shutdown *)
        IF NOT bSystemEnable THEN
            iState := 40;
        END_IF;

    40: (* SHUTDOWN SEQUENCE *)
        bSystemReady := FALSE;
        rTorchPowerDemand_MW := rTorchPowerDemand_MW - 0.5;
        
        IF rTorchPowerDemand_MW <= 0.0 THEN
            rTorchPowerDemand_MW := 0.0;
            iState := 0;
        END_IF;

    999: (* FAULT HANDLING *)
        IF NOT bEmergencyStop THEN
            (* Wait for safety reset *)
            iState := 999; 
        ELSE
            IF NOT bSystemEnable THEN
                bCriticalAlarm := FALSE;
                iState := 0;
            END_IF;
        END_IF;

END_CASE;

iOperatingState := iState;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
