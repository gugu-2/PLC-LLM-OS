import os, json, uuid
os.makedirs("data/swarm_raw", exist_ok=True)
prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: High-Altitude Pseudo-Satellite (HAPS) Solar Power Management**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Stratospheric thermal battery heating optimization, multi-zone solar array MPPT tracking, and diurnal power distribution shifting). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_HAPS_PowerManagement\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: High-Altitude Pseudo-Satellite (HAPS) Solar Power Management

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_HAPS_PowerManagement
(*=============================================================================
  Block: FB_HAPS_PowerManagement
  Description: High-Altitude Pseudo-Satellite (HAPS) Solar Power Management
  Author: 40-Year Veteran Automation Architect
  Version: 1.0.0
  Notes: Multi-zone solar array MPPT tracking, thermal battery heating optimization,
         and diurnal power distribution shifting.
=============================================================================*)
VAR_INPUT
    bSystemEnable       : BOOL;     (* System master enable signal *)
    bEmergencyStop      : BOOL;     (* Safety relay OK / emergency stop interlock *)
    rSolarIrradiance    : REAL;     (* Solar irradiance sensor (W/m^2) *)
    rTempStratosphere   : REAL;     (* Ambient external temperature in Stratosphere (Deg C) *)
    rBatteryTemp        : REAL;     (* Internal battery pack temperature (Deg C) *)
    rBatterySOC         : REAL;     (* Battery State of Charge (%) *)
    rBusVoltage         : REAL;     (* Main DC bus voltage (V) *)
    rAltitude           : REAL;     (* Current HAPS altitude (m) *)
END_VAR
VAR_OUTPUT
    bSystemReady        : BOOL;     (* Power management system is ready and nominal *)
    rMPPT_DutyCycle     : REAL;     (* PWM duty cycle for MPPT controllers (0.0 to 1.0) *)
    rHeaterControl      : REAL;     (* Analog control signal for battery thermal management *)
    rLoadShedding       : REAL;     (* Permitted payload power availability (%) *)
    bAlarm              : BOOL;     (* Master fault/alarm output *)
    iFaultCode          : INT;      (* Specific fault code identification *)
END_VAR
VAR
    iState              : INT := 0; (* Internal state machine state *)
    tStartupDelay       : TON;      (* Delay timer for system initialization *)
    tFaultTimer         : TON;      (* Timer to filter transient faults *)
    rFilteredIrradiance : REAL := 0.0;
    rAlpha              : REAL := 0.1; (* Low pass filter coefficient *)
    bCriticalFault      : BOOL := FALSE;
END_VAR

(* === MAIN LOGIC === *)
(* Emergency Stop Interlock Check *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bAlarm := TRUE;
    iFaultCode := 9999; (* E-STOP Activated *)
    rMPPT_DutyCycle := 0.0;
    rHeaterControl := 0.0;
    rLoadShedding := 0.0;
    iState := 0;
    RETURN;
END_IF;

(* Input Filtering (Noise reduction for high altitude sensors) *)
rFilteredIrradiance := rFilteredIrradiance + rAlpha * (rSolarIrradiance - rFilteredIrradiance);

(* State Machine for Power Management Control Flow *)
CASE iState OF
    0: (* IDLE & INITIALIZATION *)
        bSystemReady := FALSE;
        rMPPT_DutyCycle := 0.0;
        rHeaterControl := 0.0;
        bAlarm := FALSE;
        iFaultCode := 0;
        
        IF bSystemEnable THEN
            tStartupDelay(IN := TRUE, PT := T#10S);
            IF tStartupDelay.Q THEN
                tStartupDelay(IN := FALSE);
                iState := 10;
            END_IF;
        ELSE
            tStartupDelay(IN := FALSE);
        END_IF;

    10: (* NOMINAL OPERATIONS - MPPT & THERMAL CONTROL *)
        bSystemReady := TRUE;
        
        (* MPPT Logic based on irradiance and battery SOC *)
        IF rFilteredIrradiance > 100.0 AND rBatterySOC < 98.0 THEN
            (* Basic P-Control for MPPT Duty Cycle simulating perturbation *)
            rMPPT_DutyCycle := 0.85 + (100.0 - rBatterySOC) * 0.001;
            IF rMPPT_DutyCycle > 0.95 THEN
                rMPPT_DutyCycle := 0.95;
            END_IF;
        ELSE
            rMPPT_DutyCycle := 0.05; (* Float state *)
        END_IF;

        (* Stratospheric Thermal Battery Heating Optimization *)
        IF rBatteryTemp < 5.0 THEN
            rHeaterControl := 1.0; (* Full heat *)
        ELSIF rBatteryTemp < 15.0 THEN
            rHeaterControl := (15.0 - rBatteryTemp) / 10.0; (* Proportional heat *)
        ELSE
            rHeaterControl := 0.0; (* Optimal temp reached *)
        END_IF;
        
        (* Diurnal Power Distribution and Load Shedding *)
        IF rBatterySOC < 20.0 THEN
            rLoadShedding := 0.1; (* Critical ops only *)
        ELSIF rBatterySOC < 50.0 THEN
            rLoadShedding := 0.5; (* Half payload *)
        ELSE
            rLoadShedding := 1.0; (* Full payload available *)
        END_IF;
        
        (* Fault Detection Transition *)
        IF rBusVoltage < 22.0 OR rBatteryTemp > 45.0 THEN
            iState := 20;
        END_IF;

    20: (* FAULT HANDLING & RECOVERY *)
        bSystemReady := FALSE;
        rLoadShedding := 0.0; (* Shed all non-essential loads immediately *)
        tFaultTimer(IN := TRUE, PT := T#5S);
        
        IF tFaultTimer.Q THEN
            bAlarm := TRUE;
            IF rBusVoltage < 22.0 THEN
                iFaultCode := 101; (* Bus Under-voltage *)
            ELSIF rBatteryTemp > 45.0 THEN
                iFaultCode := 102; (* Battery Thermal Runaway *)
            END_IF;
            bCriticalFault := TRUE;
        END_IF;
        
        (* Auto-recovery condition *)
        IF rBusVoltage > 24.0 AND rBatteryTemp < 35.0 AND NOT bCriticalFault THEN
            tFaultTimer(IN := FALSE);
            bAlarm := FALSE;
            iFaultCode := 0;
            iState := 10;
        END_IF;
        
        (* Reset logic *)
        IF NOT bSystemEnable THEN
            bCriticalFault := FALSE;
            tFaultTimer(IN := FALSE);
            iState := 0;
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
