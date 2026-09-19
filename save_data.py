import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Advanced Composites Resin Transfer Molding (RTM) Vacuum Assist and Injection Pressure**

Task: Invent a highly complex, ultra-realistic control scenario for this domain. Make this code EVEN BETTER, MORE ADVANCED, and MORE RIGOROUS than previous iterations. Include extreme edge-case handling, advanced math, and robust fault-tolerance.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Composites_RTMMolding\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Advanced Composites Resin Transfer Molding (RTM) Vacuum Assist and Injection Pressure

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_RTM_VacuumInjectionControl
(* 
   Advanced Composites Resin Transfer Molding (RTM) Vacuum Assist and Injection Pressure Controller
   Implements multi-stage vacuum profiling, dynamic injection pressure control with cavity pressure feedback,
   resin flow-front tracking, and real-time fault detection.
*)
VAR_INPUT
    bEnable                 : BOOL;     (* System Enable *)
    bEmergencyStop          : BOOL;     (* E-Stop safety interlock, normally closed *)
    rMoldTemp               : REAL;     (* Mold temperature (deg C) *)
    rResinTemp              : REAL;     (* Resin temperature (deg C) *)
    rCavityPressure         : REAL;     (* Internal cavity pressure (bar) *)
    rVacuumLevel            : REAL;     (* Current vacuum level (mbar) *)
    rResinViscosity         : REAL;     (* Real-time resin viscosity reading (cP) *)
    rFlowFrontPosition      : REAL;     (* Flow front progression (0.0 to 1.0) *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* System is ready for injection cycle *)
    rVacuumValveCmd         : REAL;     (* Vacuum valve position command (0-100%) *)
    rInjectionPressureCmd   : REAL;     (* Injection pump pressure setpoint (bar) *)
    rHeatingPowerCmd        : REAL;     (* Mold heating power output (0-100%) *)
    bInjectionComplete      : BOOL;     (* Injection cycle successfully completed *)
    bAlarmFault             : BOOL;     (* General fault alarm *)
    iFaultCode              : INT;      (* Diagnostics fault code *)
END_VAR
VAR
    iState                  : INT := 0; 
    tCycleTimer             : TON;
    tDwellTimer             : TON;
    rFilteredCavityPress    : REAL;
    rErrorPressure          : REAL;
    rIntegralPressure       : REAL;
    rDerivativePressure     : REAL;
    rPrevErrorPressure      : REAL;
    
    (* PID Constants *)
    Kp                      : REAL := 2.5;
    Ki                      : REAL := 0.8;
    Kd                      : REAL := 0.1;
    
    (* Thresholds *)
    rMaxSafePressure        : REAL := 15.0; (* bar *)
    rMinVacuum              : REAL := 5.0;  (* mbar *)
END_VAR

(* --- SAFETY INTERLOCKS --- *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    rVacuumValveCmd := 0.0;
    rInjectionPressureCmd := 0.0;
    rHeatingPowerCmd := 0.0;
    bAlarmFault := TRUE;
    iFaultCode := 999; (* E-STOP Activated *)
    iState := 0;
    RETURN;
END_IF;

(* --- SENSOR FILTERING (Simple Exponential Moving Average) --- *)
rFilteredCavityPress := (0.1 * rCavityPressure) + (0.9 * rFilteredCavityPress);

(* --- MAIN STATE MACHINE --- *)
CASE iState OF
    0: (* IDLE & PRE-CHECK *)
        bSystemReady := FALSE;
        bInjectionComplete := FALSE;
        rVacuumValveCmd := 0.0;
        rInjectionPressureCmd := 0.0;
        bAlarmFault := FALSE;
        iFaultCode := 0;
        
        (* Check if temperatures are within tolerance before proceeding *)
        IF bEnable AND (rMoldTemp > 80.0) AND (rMoldTemp < 120.0) AND (rResinTemp > 40.0) THEN
            iState := 10;
        ELSIF bEnable THEN
            bAlarmFault := TRUE;
            iFaultCode := 101; (* Temperature out of range *)
        END_IF;

    10: (* VACUUM DRAWDOWN *)
        bSystemReady := TRUE;
        rVacuumValveCmd := 100.0; (* Open vacuum valve fully *)
        
        tCycleTimer(IN := TRUE, PT := T#60S);
        
        IF rVacuumLevel < rMinVacuum THEN
            tCycleTimer(IN := FALSE);
            iState := 20; (* Vacuum achieved *)
        ELSIF tCycleTimer.Q THEN
            tCycleTimer(IN := FALSE);
            bAlarmFault := TRUE;
            iFaultCode := 102; (* Vacuum timeout - possible leak *)
            iState := 0;
        END_IF;
        
    20: (* INJECTION PROFILE *)
        rVacuumValveCmd := 20.0; (* Maintain slight vacuum assist *)
        
        (* PID Control for Injection Pressure based on Flow Front & Cavity Pressure *)
        rErrorPressure := 5.0 - rFilteredCavityPress; (* Target 5.0 bar internal pressure *)
        rIntegralPressure := rIntegralPressure + rErrorPressure;
        rDerivativePressure := rErrorPressure - rPrevErrorPressure;
        
        rInjectionPressureCmd := (Kp * rErrorPressure) + (Ki * rIntegralPressure) + (Kd * rDerivativePressure);
        
        (* Saturation limits *)
        IF rInjectionPressureCmd > 10.0 THEN
            rInjectionPressureCmd := 10.0;
        ELSIF rInjectionPressureCmd < 0.0 THEN
            rInjectionPressureCmd := 0.0;
        END_IF;
        
        rPrevErrorPressure := rErrorPressure;
        
        (* Safety Limit Check *)
        IF rFilteredCavityPress > rMaxSafePressure THEN
            bAlarmFault := TRUE;
            iFaultCode := 201; (* Overpressure anomaly *)
            rInjectionPressureCmd := 0.0;
            iState := 0;
        END_IF;
        
        (* Viscosity spike indicates premature curing *)
        IF rResinViscosity > 1500.0 THEN
            bAlarmFault := TRUE;
            iFaultCode := 202; (* Premature gelation detected *)
            rInjectionPressureCmd := 0.0;
            iState := 0;
        END_IF;
        
        IF rFlowFrontPosition >= 0.98 THEN
            (* Mold is full *)
            rInjectionPressureCmd := 0.0;
            rVacuumValveCmd := 0.0;
            iState := 30;
        END_IF;

    30: (* POST-FILL DWELL / CURE *)
        tDwellTimer(IN := TRUE, PT := T#300S); (* 5 minute dwell *)
        rHeatingPowerCmd := 80.0; (* Maintain cure temp *)
        
        IF tDwellTimer.Q THEN
            tDwellTimer(IN := FALSE);
            bInjectionComplete := TRUE;
            rHeatingPowerCmd := 0.0;
            iState := 40;
        END_IF;
        
    40: (* CYCLE COMPLETE *)
        IF NOT bEnable THEN
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

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
