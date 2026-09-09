import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Deep-Space Nuclear Thermal Propulsion (NTP) Bimodal Reactor**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Gaseous hydrogen propellant expansion, enriched uranium fuel element thermal balancing, and Brayton cycle power generation phase switching). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_NTP_BimodalReactor\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Deep-Space Nuclear Thermal Propulsion (NTP) Bimodal Reactor

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_NTP_BimodalReactor
VAR_INPUT
    (* Safety & Interlock Inputs *)
    bEnable                 : BOOL;     (* System enable signal from master controller *)
    bScramSystem            : BOOL;     (* Hardware scram / Emergency stop OK signal (Active High) *)
    
    (* Physical Measurements *)
    rCoreTempMain_K         : REAL;     (* Reactor core temperature [Kelvin] *)
    rPropFlowRate_kg_s      : REAL;     (* Hydrogen propellant flow rate [kg/s] *)
    rNeutronFlux            : REAL;     (* Ex-core neutron flux measurement [nv] *)
    
    (* Operational Modes *)
    bRequestPropulsion      : BOOL;     (* Request for high-thrust NTP mode *)
    bRequestBraytonPower    : BOOL;     (* Request for closed-loop Brayton power generation mode *)
END_VAR
VAR_OUTPUT
    (* System Status Outputs *)
    bSystemReady            : BOOL;     (* System ready for operation status *)
    bCriticalAlarm          : BOOL;     (* Core anomaly or safety threshold exceeded *)
    bPropulsionActive       : BOOL;     (* High-thrust propulsion mode is engaged *)
    bBraytonActive          : BOOL;     (* Brayton power generation mode is engaged *)
    
    (* Actuator Control Signals *)
    rControlDrumAngle_deg   : REAL;     (* Commanded reflector control drum angle [degrees] 0-180 *)
    rPropValvePosition_pct  : REAL;     (* Propellant flow control valve position [0-100%] *)
    rBraytonBypass_pct      : REAL;     (* Brayton cycle turbine bypass valve position [0-100%] *)
END_VAR
VAR
    (* Internal state variables *)
    iReactorState           : INT := 0; (* State Machine Index *)
    
    (* Timers and Filters *)
    tStartupDelay           : TON;      (* Startup sequence delay timer *)
    tModeSwitchDelay        : TON;      (* Delay for thermal stabilization during mode switch *)
    
    (* Internal Control Variables *)
    rFilteredCoreTemp       : REAL;     (* First-order filtered core temperature *)
    rThermalSetpoint        : REAL;     (* Target temperature setpoint based on active mode *)
    rDrumAngleIntegral      : REAL;     (* Integral accumulator for reactivity control *)
    
    (* Constants *)
    MAX_CORE_TEMP           : REAL := 2800.0; (* Maximum allowable core temperature in Kelvin *)
    MAX_BRAYTON_TEMP        : REAL := 1500.0; (* Maximum temperature for power generation mode *)
END_VAR

(* === MAIN LOGIC === *)

(* 1. Safety and Scram Interlock Processing *)
IF NOT bScramSystem THEN
    (* Immediate SCRAM: Rotate drums to minimum reactivity, close valves, flag alarm *)
    rControlDrumAngle_deg := 0.0; 
    rPropValvePosition_pct := 0.0;
    rBraytonBypass_pct := 100.0; (* Bypass turbine fully during scram *)
    bSystemReady := FALSE;
    bCriticalAlarm := TRUE;
    bPropulsionActive := FALSE;
    bBraytonActive := FALSE;
    iReactorState := 0;
    RETURN;
END_IF;

(* 2. Core Temperature Filtering & Protection *)
(* Simple first-order low pass filter logic (simulated representation) *)
rFilteredCoreTemp := (rFilteredCoreTemp * 0.9) + (rCoreTempMain_K * 0.1);

IF rFilteredCoreTemp > MAX_CORE_TEMP THEN
    bCriticalAlarm := TRUE;
    (* Initiate protective power reduction *)
    rControlDrumAngle_deg := 10.0;
ELSE
    bCriticalAlarm := FALSE;
END_IF;

(* 3. Primary State Machine *)
CASE iReactorState OF
    0: (* IDLE / SHUTDOWN STATE *)
        bSystemReady := FALSE;
        rControlDrumAngle_deg := 0.0;
        rPropValvePosition_pct := 0.0;
        
        IF bEnable THEN
            tStartupDelay(IN := TRUE, PT := T#10S);
            IF tStartupDelay.Q THEN
                tStartupDelay(IN := FALSE);
                iReactorState := 10; (* Move to STANDBY *)
            END_IF;
        ELSE
            tStartupDelay(IN := FALSE);
        END_IF;

    10: (* STANDBY STATE *)
        bSystemReady := TRUE;
        bPropulsionActive := FALSE;
        bBraytonActive := FALSE;
        
        (* Maintain sub-critical keeping power *)
        rControlDrumAngle_deg := 45.0; 
        rPropValvePosition_pct := 5.0; (* Trickle flow for cooling *)
        rBraytonBypass_pct := 100.0;

        IF bRequestPropulsion THEN
            iReactorState := 20; (* Transition to Propulsion *)
        ELSIF bRequestBraytonPower THEN
            iReactorState := 30; (* Transition to Power Generation *)
        END_IF;
        
        IF NOT bEnable THEN
            iReactorState := 0;
        END_IF;

    20: (* PROPULSION MODE *)
        bPropulsionActive := TRUE;
        bBraytonActive := FALSE;
        rThermalSetpoint := 2500.0; (* High temperature for max Isp *)
        
        (* Simulated PI Control for Drum Angle based on Temperature Setpoint *)
        IF rFilteredCoreTemp < rThermalSetpoint THEN
            rDrumAngleIntegral := rDrumAngleIntegral + 0.1;
        ELSE
            rDrumAngleIntegral := rDrumAngleIntegral - 0.1;
        END_IF;
        
        (* Clamp Integral *)
        IF rDrumAngleIntegral > 140.0 THEN rDrumAngleIntegral := 140.0; END_IF;
        IF rDrumAngleIntegral < 45.0 THEN rDrumAngleIntegral := 45.0; END_IF;
        
        rControlDrumAngle_deg := rDrumAngleIntegral;
        
        (* Match propellant flow to core temperature to avoid thermal shock *)
        rPropValvePosition_pct := (rFilteredCoreTemp / MAX_CORE_TEMP) * 100.0;
        
        IF NOT bRequestPropulsion THEN
            iReactorState := 10;
        END_IF;

    30: (* BRAYTON POWER GENERATION MODE *)
        bPropulsionActive := FALSE;
        bBraytonActive := TRUE;
        rThermalSetpoint := 1400.0; (* Lower temp for long-duration closed loop power *)
        
        (* Modulate drums for lower steady-state power *)
        rControlDrumAngle_deg := 85.0; 
        
        (* Direct working fluid to turbines *)
        rBraytonBypass_pct := 0.0;
        rPropValvePosition_pct := 10.0; (* Minimum makeup flow *)
        
        IF NOT bRequestBraytonPower THEN
            iReactorState := 10;
        END_IF;
        
    ELSE
        (* FAULT RECOVERY *)
        iReactorState := 0;
        
END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs('data/swarm_raw', exist_ok=True)
record = {'messages': [{'role': 'user', 'content': prompt}, {'role': 'assistant', 'content': code}]}
filepath = f'data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json'
with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(record, f, ensure_ascii=False)

print(f'Saved to {filepath}')
