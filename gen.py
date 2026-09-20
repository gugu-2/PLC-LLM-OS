import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V4 Persona: a 50+ years experienced Chief PLC Architect & Control Systems PhD. 
Your logic must include advanced Non-Linear PID with Anti-Windup, 3-level cascade control, digital low-pass filtering, predictive anomaly detection, and multi-layered hardware interlocks. Output the most elite, mathematically rigorous, and structurally flawless IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Mega-Scale Data Center Immersion Cooling Two-Phase Dielectric Fluid Boiling Point and Condenser Sync**

Task: Invent a highly complex, ultra-realistic control scenario for this domain. This MUST be drastically better, more advanced, and longer than previous iterations.

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
3. LENGTH: The assistant content MUST be >= 2000 characters total. Make it massive and extremely rigorous.
4. SAVE to isolated file using this exact Python:
   import json, uuid
   prompt = \"\"\"<copy this exact user prompt here>\"\"\"
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_DataCenter_ImmersionCooling\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
   record = {\"messages\": [{\"role\": \"user\", \"content\": prompt}, {\"role\": \"assistant\", \"content\": code}]}
   with open(f\"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json\", \"w\", encoding=\"utf-8\") as f:
       json.dump(record, f, ensure_ascii=False)
5. SELF-CHECK before saving - verify ALL:
   [ ] Fence is ```iec-st
   [ ] First code line: FUNCTION_BLOCK FB_<name>
   [ ] Has VAR_INPUT & VAR_OUTPUT sections
   [ ] Has END_IF; or END_CASE;
   [ ] Last code line: END_FUNCTION_BLOCK
   [ ] Closing fence: ```
   [ ] Total chars >= 2000
6. REPLY with: EVOLUTION COMPLETE: Mega-Scale Data Center Immersion Cooling Two-Phase Dielectric Fluid Boiling Point and Condenser Sync"""

code = """```iec-st
FUNCTION_BLOCK FB_ImmersionCoolingSync
VAR_INPUT
    (* System Enable and Safety *)
    bSystemEnable           : BOOL;     (* Master enable for the cooling system *)
    bEmergencyStop          : BOOL;     (* Emergency stop circuit OK (True = OK) *)
    bLeakDetected           : BOOL;     (* Fluid leak detection signal *)
    bPowerGridStable        : BOOL;     (* Utility grid stability indicator *)
    bMaintenanceMode        : BOOL;     (* System in maintenance, overrides cooling *)
    bFireAlarm              : BOOL;     (* Data center fire alarm interlock *)
    
    (* Process Variables - Two-Phase Tank *)
    rDielectricTemp_C       : REAL;     (* Bulk dielectric fluid temperature [°C] *)
    rDielectricPressure_kPa : REAL;     (* Tank pressure [kPa] *)
    rLiquidLevel_mm         : REAL;     (* Tank liquid level [mm] *)
    rITHeatLoad_kW          : REAL;     (* Aggregated server heat load [kW] *)
    
    (* Process Variables - Condenser Circuit *)
    rCondenserWaterSupply_C : REAL;     (* Condenser water supply temperature [°C] *)
    rCondenserWaterReturn_C : REAL;     (* Condenser water return temperature [°C] *)
    rCondenserFlow_LPM      : REAL;     (* Primary condenser flow rate [LPM] *)
    
    (* Tuning Parameters *)
    rBoilingPointSetpt_C    : REAL;     (* Target boiling point control setpoint [°C] *)
    rPressureSetpt_kPa      : REAL;     (* Target pressure setpoint [kPa] *)
    rFilterTimeConst_s      : REAL;     (* Digital low-pass filter time constant [s] *)
END_VAR

VAR_OUTPUT
    (* Actuator Controls *)
    rCondenserValvePos_pct  : REAL;     (* Condenser water flow control valve [0-100%] *)
    rVaporRecoveryPump_Hz   : REAL;     (* Vapor recovery pump VFD speed [Hz] *)
    rFluidMakeUpValve_pct   : REAL;     (* Fluid make-up valve position [0-100%] *)
    
    (* System Status and Alarms *)
    bSystemReady            : BOOL;     (* System is initialized and ready *)
    bActiveCooling          : BOOL;     (* System is actively cooling IT load *)
    bAlarmCritical          : BOOL;     (* Critical alarm (e.g., pressure high, leak) *)
    bAlarmWarning           : BOOL;     (* Warning alarm (e.g., filter deviation) *)
    iOperatingState         : INT;      (* Current state machine step *)
END_VAR

VAR
    (* Internal State *)
    iState                  : INT := 0;
    
    (* Filtered Process Variables *)
    rFiltTemp               : REAL;
    rFiltPress              : REAL;
    
    (* PID Controllers *)
    rPressError             : REAL;
    rPressIntegral          : REAL;
    rPressDerivative        : REAL;
    rLastPressError         : REAL;
    
    rTempError              : REAL;
    rTempIntegral           : REAL;
    rTempDerivative         : REAL;
    rLastTempError          : REAL;
    
    (* Timers *)
    tStartupDelay           : TON;
    tStabilizationTimer     : TON;
    tSafetyTimeout          : TON;
    
    (* Anti-Windup Limits *)
    rIntegralMax            : REAL := 100.0;
    rIntegralMin            : REAL := -100.0;
    
    (* Cycle Time *)
    rCycleTime_s            : REAL := 0.1; (* Assumed 100ms task *)
END_VAR

(* === SAFETY & INTERLOCKS === *)
IF NOT bEmergencyStop OR bLeakDetected OR NOT bPowerGridStable OR bFireAlarm THEN
    (* Immediate shutdown on critical safety loss *)
    rCondenserValvePos_pct := 100.0; (* Fail open for maximum cooling *)
    rVaporRecoveryPump_Hz := 0.0;
    rFluidMakeUpValve_pct := 0.0;
    
    bSystemReady := FALSE;
    bActiveCooling := FALSE;
    bAlarmCritical := TRUE;
    
    iState := 999; (* FAULT STATE *)
    iOperatingState := iState;
    RETURN;
END_IF;

(* === DIGITAL LOW-PASS FILTERING === *)
(* First-order lag filters for noisy process variables *)
rFiltTemp := rFiltTemp + (rCycleTime_s / (rFilterTimeConst_s + rCycleTime_s)) * (rDielectricTemp_C - rFiltTemp);
rFiltPress := rFiltPress + (rCycleTime_s / (rFilterTimeConst_s + rCycleTime_s)) * (rDielectricPressure_kPa - rFiltPress);

(* === MAIN STATE MACHINE === *)
CASE iState OF
    0: (* IDLE & INITIALIZATION *)
        bSystemReady := FALSE;
        bActiveCooling := FALSE;
        bAlarmCritical := FALSE;
        rCondenserValvePos_pct := 0.0;
        rVaporRecoveryPump_Hz := 0.0;
        
        IF bSystemEnable AND NOT bMaintenanceMode THEN
            tStartupDelay(IN := TRUE, PT := T#5S);
            IF tStartupDelay.Q THEN
                tStartupDelay(IN := FALSE);
                bSystemReady := TRUE;
                iState := 10;
            END_IF;
        ELSE
            tStartupDelay(IN := FALSE);
        END_IF;
        
    10: (* STANDBY / PRE-START CHECK *)
        IF rLiquidLevel_mm < 500.0 THEN
            bAlarmWarning := TRUE;
            rFluidMakeUpValve_pct := 50.0; (* Start filling *)
        ELSE
            bAlarmWarning := FALSE;
            rFluidMakeUpValve_pct := 0.0;
            IF rITHeatLoad_kW > 10.0 THEN (* IT Load detected *)
                iState := 20;
            END_IF;
        END_IF;
        
        IF NOT bSystemEnable THEN
            iState := 0;
        END_IF;

    20: (* RAMP UP & CASCADE CONTROL (PRESSURE -> TEMPERATURE -> VALVE) *)
        bActiveCooling := TRUE;
        
        (* Outer Loop: Pressure Control (Maintains 2-Phase Boiling Point via Pressure) *)
        rPressError := rPressureSetpt_kPa - rFiltPress;
        rPressIntegral := rPressIntegral + (rPressError * rCycleTime_s);
        
        (* Anti-windup for Outer Loop *)
        IF rPressIntegral > rIntegralMax THEN rPressIntegral := rIntegralMax; END_IF;
        IF rPressIntegral < rIntegralMin THEN rPressIntegral := rIntegralMin; END_IF;
        
        rPressDerivative := (rPressError - rLastPressError) / rCycleTime_s;
        rLastPressError := rPressError;
        
        (* Calculate cascade setpoint for temperature based on pressure deviation *)
        (* Assume Kp = 0.5, Ki = 0.1, Kd = 0.05 for pressure to temp cascade *)
        rBoilingPointSetpt_C := rBoilingPointSetpt_C + (0.5 * rPressError + 0.1 * rPressIntegral + 0.05 * rPressDerivative);
        
        (* Inner Loop: Temperature Control (Actuates Condenser Valve) *)
        rTempError := rFiltTemp - rBoilingPointSetpt_C; (* Reverse acting for cooling *)
        rTempIntegral := rTempIntegral + (rTempError * rCycleTime_s);
        
        (* Anti-windup for Inner Loop *)
        IF rTempIntegral > rIntegralMax THEN rTempIntegral := rIntegralMax; END_IF;
        IF rTempIntegral < 0.0 THEN rTempIntegral := 0.0; END_IF; (* Unidirectional cooling *)
        
        rTempDerivative := (rTempError - rLastTempError) / rCycleTime_s;
        rLastTempError := rTempError;
        
        (* Assume Kp = 2.0, Ki = 0.5, Kd = 0.1 for temp to valve cascade *)
        rCondenserValvePos_pct := (2.0 * rTempError) + (0.5 * rTempIntegral) + (0.1 * rTempDerivative);
        
        (* Feedforward Control: Anticipate load changes *)
        rCondenserValvePos_pct := rCondenserValvePos_pct + (rITHeatLoad_kW * 0.1); 
        
        (* Valve saturation limits *)
        IF rCondenserValvePos_pct > 100.0 THEN rCondenserValvePos_pct := 100.0; END_IF;
        IF rCondenserValvePos_pct < 0.0 THEN rCondenserValvePos_pct := 0.0; END_IF;
        
        (* Vapor Recovery Logic based on Pressure *)
        IF rFiltPress > (rPressureSetpt_kPa * 1.1) THEN
            rVaporRecoveryPump_Hz := 50.0; (* Max recovery speed *)
        ELSIF rFiltPress > (rPressureSetpt_kPa * 1.05) THEN
            rVaporRecoveryPump_Hz := 30.0; (* Partial recovery speed *)
        ELSE
            rVaporRecoveryPump_Hz := 10.0; (* Idle / baseline recovery *)
        END_IF;

        IF rITHeatLoad_kW <= 5.0 THEN
            tStabilizationTimer(IN := TRUE, PT := T#60S);
            IF tStabilizationTimer.Q THEN
                tStabilizationTimer(IN := FALSE);
                iState := 10; (* Return to standby *)
            END_IF;
        ELSE
            tStabilizationTimer(IN := FALSE);
        END_IF;
        
        IF NOT bSystemEnable THEN
            iState := 0;
        END_IF;

    999: (* FAULT STATE *)
        bSystemReady := FALSE;
        bActiveCooling := FALSE;
        rCondenserValvePos_pct := 100.0; (* Fail safe: max cooling *)
        rVaporRecoveryPump_Hz := 0.0;
        rFluidMakeUpValve_pct := 0.0;
        
        IF bSystemEnable = FALSE AND bEmergencyStop AND NOT bLeakDetected AND bPowerGridStable AND NOT bFireAlarm THEN
            (* Manual reset required *)
            iState := 0;
        END_IF;
        
END_CASE;

iOperatingState := iState;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
