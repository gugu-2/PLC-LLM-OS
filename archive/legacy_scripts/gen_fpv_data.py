import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Next-Gen Utility-Scale Offshore Floating Solar Photovoltaic (FPV) Array**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Wave-induced dynamic structural tension compensation, saline corrosive mist active insulator washing, and multi-inverter decentralized MPPT power smoothing). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_FloatingSolar_Array\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Next-Gen Utility-Scale Offshore Floating Solar Photovoltaic (FPV) Array

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_FPV_ArrayController
(* 
   =============================================================================
   Lumina AI Cloud Swarm - Elite Automation Code
   Domain: Next-Gen Utility-Scale Offshore Floating Solar Photovoltaic (FPV) Array
   Description: Advanced active structural tension compensation, multi-inverter 
                MPPT coordination, and automated saline mist washing control.
                Incorporates robust noise filtering (EMA), layered safety interlocks, 
                and comprehensive state-machine resilience for harsh marine environments.
   =============================================================================
*)

VAR_INPUT
    bEnable                 : BOOL;     (* System global enable command *)
    bEmergencyStop          : BOOL;     (* E-Stop safety loop (Normally Closed, True = OK) *)
    bGridFault              : BOOL;     (* Main grid fault indication from substation *)
    rWaveAmplitude_m        : REAL;     (* Sea state monitoring: Wave amplitude in meters (Lidar/Sonar) *)
    rWaveFrequency_Hz       : REAL;     (* Sea state monitoring: Wave frequency in Hz *)
    rStructuralTension_kN   : REAL;     (* Strain gauge reading: Anchor line tension in kilonewtons *)
    rSolarIrradiance_Wm2    : REAL;     (* Pyranometer reading: W/m^2 *)
    rInverterTemp_C         : REAL;     (* Critical inverter average temperature in deg C *)
    rSalinitySensor_ppm     : REAL;     (* Insulator surface saline accumulation in ppm *)
END_VAR

VAR_OUTPUT
    bSystemReady            : BOOL;     (* System is initialized, safe, and ready for power generation *)
    bActiveCompensation     : BOOL;     (* Dynamic tension compensation mechanism is active *)
    rTensionWinchCmd_Pct    : REAL;     (* Command to anchor tensioning winches (0.0 to 100.0%) *)
    rInverterPowerLimit_Pct : REAL;     (* Curtailed power setpoint for multi-inverter MPPT smoothing *)
    bWashSystemActive       : BOOL;     (* Trigger for fresh-water spray to clean saline mist *)
    bCriticalAlarm          : BOOL;     (* Critical structural or electrical fault - requires intervention *)
END_VAR

VAR
    (* State Machine *)
    iState                  : INT := 0; (* 0: INIT, 10: IDLE, 20: PRE-CHARGE, 30: GENERATING, 40: WASHING, 99: FAULT *)
    
    (* Internal Timers *)
    tWashTimer              : TON;
    tTensionSettleTimer     : TON;
    tFaultFilter            : TON;
    
    (* Filter Variables *)
    rFilteredTension        : REAL := 0.0;
    rFilteredIrradiance     : REAL := 0.0;
    
    (* Constants *)
    TENSION_MAX_KN          : REAL := 2500.0;
    TENSION_TARGET_KN       : REAL := 1200.0;
    WASH_THRESHOLD_PPM      : REAL := 1500.0;
    TEMP_DERATE_START_C     : REAL := 65.0;
    TEMP_MAX_C              : REAL := 85.0;
    ALPHA_FILTER            : REAL := 0.1; (* Exponential Moving Average filter coefficient *)
END_VAR

(* === MAIN LOGIC === *)

(* 1. Essential Safety Interlocks *)
IF NOT bEmergencyStop OR bGridFault THEN
    iState := 99; (* Force immediate transition to FAULT state *)
END_IF;

(* 2. Sensor Signal Filtering (EMA for noise rejection) *)
rFilteredTension := (ALPHA_FILTER * rStructuralTension_kN) + ((1.0 - ALPHA_FILTER) * rFilteredTension);
rFilteredIrradiance := (ALPHA_FILTER * rSolarIrradiance_Wm2) + ((1.0 - ALPHA_FILTER) * rFilteredIrradiance);

(* 3. Critical Alarm Evaluation (Structural Integrity) *)
tFaultFilter(IN := (rFilteredTension > TENSION_MAX_KN) OR (rInverterTemp_C > TEMP_MAX_C), PT := T#2S);
IF tFaultFilter.Q THEN
    bCriticalAlarm := TRUE;
    iState := 99;
ELSE
    bCriticalAlarm := FALSE;
END_IF;

(* 4. State Machine Operation *)
CASE iState OF
    0: (* INIT - System startup and sensor baseline calibration *)
        bSystemReady := FALSE;
        bActiveCompensation := FALSE;
        rTensionWinchCmd_Pct := 0.0;
        rInverterPowerLimit_Pct := 0.0;
        bWashSystemActive := FALSE;
        
        IF bEnable AND bEmergencyStop THEN
            iState := 10;
        END_IF;
        
    10: (* IDLE - Waiting for solar irradiance or wave action *)
        bSystemReady := TRUE;
        rInverterPowerLimit_Pct := 0.0;
        
        IF rFilteredIrradiance > 150.0 THEN
            iState := 20;
        END_IF;
        
        IF rSalinitySensor_ppm > WASH_THRESHOLD_PPM THEN
            iState := 40;
        END_IF;

    20: (* PRE-CHARGE - Soft start inverters *)
        rInverterPowerLimit_Pct := 20.0; (* Limit to 20% during synchronization *)
        tTensionSettleTimer(IN := TRUE, PT := T#10S);
        IF tTensionSettleTimer.Q THEN
            tTensionSettleTimer(IN := FALSE);
            iState := 30;
        END_IF;
        
    30: (* GENERATING - Active MPPT and Dynamic Tension Control *)
        (* Power smoothing and thermal derating *)
        IF rInverterTemp_C > TEMP_DERATE_START_C THEN
            rInverterPowerLimit_Pct := 100.0 - ((rInverterTemp_C - TEMP_DERATE_START_C) * 5.0);
            IF rInverterPowerLimit_Pct < 10.0 THEN
                rInverterPowerLimit_Pct := 10.0;
            END_IF;
        ELSE
            rInverterPowerLimit_Pct := 100.0;
        END_IF;
        
        (* Dynamic Wave Tension Compensation (Proportional response) *)
        IF rWaveAmplitude_m > 1.5 THEN
            bActiveCompensation := TRUE;
            rTensionWinchCmd_Pct := (rFilteredTension - TENSION_TARGET_KN) * 0.05;
            (* Clamp command *)
            IF rTensionWinchCmd_Pct > 100.0 THEN rTensionWinchCmd_Pct := 100.0; END_IF;
            IF rTensionWinchCmd_Pct < 0.0 THEN rTensionWinchCmd_Pct := 0.0; END_IF;
        ELSE
            bActiveCompensation := FALSE;
            rTensionWinchCmd_Pct := 0.0;
        END_IF;
        
        (* Check wash condition *)
        IF rSalinitySensor_ppm > WASH_THRESHOLD_PPM THEN
            iState := 40;
        END_IF;
        
        (* Check low irradiance *)
        IF rFilteredIrradiance < 50.0 THEN
            iState := 10;
        END_IF;

    40: (* WASHING - Active Insulator Cleaning Sequence *)
        bWashSystemActive := TRUE;
        rInverterPowerLimit_Pct := 50.0; (* Derate during washing to prevent arcing *)
        
        tWashTimer(IN := TRUE, PT := T#5M); (* Wash for 5 minutes *)
        IF tWashTimer.Q THEN
            tWashTimer(IN := FALSE);
            bWashSystemActive := FALSE;
            IF rFilteredIrradiance > 150.0 THEN
                iState := 20;
            ELSE
                iState := 10;
            END_IF;
        END_IF;

    99: (* FAULT - Safe state lock-in *)
        bSystemReady := FALSE;
        rInverterPowerLimit_Pct := 0.0;
        rTensionWinchCmd_Pct := 100.0; (* Full tension release / slack to prevent structural failure *)
        bActiveCompensation := FALSE;
        bWashSystemActive := FALSE;
        
        IF NOT bCriticalAlarm AND bEnable AND bEmergencyStop AND NOT bGridFault THEN
            iState := 0; (* Manual reset logic could go here *)
        END_IF;
        
END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
