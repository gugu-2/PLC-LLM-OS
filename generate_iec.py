import json, uuid, os
prompt = """<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Automated Commercial Laundry Continuous Batch Washer (CBW) Tunnel Chemical Dosing and Water Recovery**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_CBW_LaundryTunnel\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Automated Commercial Laundry Continuous Batch Washer (CBW) Tunnel Chemical Dosing and Water Recovery

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.
</USER_REQUEST>"""

code = """```iec-st
FUNCTION_BLOCK FB_CBW_Tunnel_Dosing_WaterRecovery
VAR_INPUT
    bSystemEnable           : BOOL;     (* Main system enable command *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal, active HIGH *)
    rInletWaterFlow         : REAL;     (* Measured fresh water inlet flow in L/min *)
    rTunnelTempZone1        : REAL;     (* Measured temperature in wash zone 1 in deg C *)
    rpH_WashZone            : REAL;     (* Measured pH in the main wash zone *)
    rConductivityRecovery   : REAL;     (* Measured conductivity of recovered water in uS/cm *)
    bLinenTransferActive    : BOOL;     (* Indicates linen batch transfer in progress *)
    bChemicalTanksLevelOK   : BOOL;     (* Minimum level switch for chemical dosing tanks *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* System is ready to accept linen batches *)
    rAlkaliDosingPumpSpeed  : REAL;     (* Control signal for alkali dosing pump in % *)
    rDetergentDosingPumpSpeed: REAL;    (* Control signal for detergent dosing pump in % *)
    bFreshWaterValveOpen    : BOOL;     (* Command to open fresh water make-up valve *)
    bRecoveryPumpRun        : BOOL;     (* Command to run the water recovery transfer pump *)
    rHeatingValvePosition   : REAL;     (* 0-100% position control for steam heating valve *)
    bAlarmCritical          : BOOL;     (* Critical fault requiring immediate operator action *)
    bWarningQuality         : BOOL;     (* Warning regarding wash quality (e.g. pH or temp off) *)
    iCurrentState           : INT;      (* Current state of the state machine *)
END_VAR
VAR
    (* Internal State and Timers *)
    iState                  : INT := 0;
    tInitializationTimer    : TON;
    tTransferDelay          : TON;
    tDosingTimeout          : TON;
    tTempStabilization      : TON;
    
    (* Filtered values and mathematical accumulators *)
    rFiltered_pH            : REAL := 7.0;
    rFiltered_Conductivity  : REAL := 0.0;
    rpH_Error               : REAL := 0.0;
    rpH_Integral            : REAL := 0.0;
    rTemp_Error             : REAL := 0.0;
    rTemp_Integral          : REAL := 0.0;
    
    (* Constants and Tuning Parameters *)
    c_pH_Setpoint           : REAL := 10.5;   (* Target pH for alkaline wash phase *)
    c_Temp_Setpoint         : REAL := 85.0;   (* Target temperature in degrees C *)
    c_Kp_pH                 : REAL := 12.5;   (* Proportional gain for pH dosing *)
    c_Ki_pH                 : REAL := 0.5;    (* Integral gain for pH dosing *)
    c_Kp_Temp               : REAL := 5.0;    (* Proportional gain for heating control *)
    c_Ki_Temp               : REAL := 0.1;    (* Integral gain for heating control *)
    c_AlphaFilter           : REAL := 0.1;    (* EWMA filter coefficient for noisy sensors *)
    
    (* Previous states for rate of change calculation *)
    rPrevpH                 : REAL := 7.0;
    rDerivativepH           : REAL := 0.0;
END_VAR

(* === MAIN LOGIC === *)
(* 1. CRITICAL SAFETY INTERLOCKS *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    rAlkaliDosingPumpSpeed := 0.0;
    rDetergentDosingPumpSpeed := 0.0;
    bFreshWaterValveOpen := FALSE;
    bRecoveryPumpRun := FALSE;
    rHeatingValvePosition := 0.0;
    bAlarmCritical := TRUE;
    iState := 999; (* Fault state *)
    iCurrentState := iState;
    RETURN;
END_IF;

(* Clear critical alarms if safety is restored but interlock system level enable is required *)
IF bAlarmCritical AND bEmergencyStop AND NOT bSystemEnable THEN
    bAlarmCritical := FALSE;
    iState := 0; (* Reset to IDLE *)
END_IF;

(* 2. SENSOR NOISE FILTERING & SIGNAL PROCESSING *)
(* Apply Exponential Weighted Moving Average (EWMA) filter to noisy analog inputs *)
rFiltered_pH := (c_AlphaFilter * rpH_WashZone) + ((1.0 - c_AlphaFilter) * rFiltered_pH);
rFiltered_Conductivity := (c_AlphaFilter * rConductivityRecovery) + ((1.0 - c_AlphaFilter) * rFiltered_Conductivity);

(* Calculate derivative for pH to predict rapid changes during chemical spikes *)
rDerivativepH := rFiltered_pH - rPrevpH;
rPrevpH := rFiltered_pH;

(* 3. STATE MACHINE CONTROL MODULE *)
CASE iState OF
    0: (* STATE 0: IDLE / STANDBY *)
        bSystemReady := FALSE;
        rAlkaliDosingPumpSpeed := 0.0;
        rDetergentDosingPumpSpeed := 0.0;
        rHeatingValvePosition := 0.0;
        bFreshWaterValveOpen := FALSE;
        bRecoveryPumpRun := FALSE;
        
        IF bSystemEnable AND bChemicalTanksLevelOK THEN
            iState := 10;
        ELSIF bSystemEnable AND NOT bChemicalTanksLevelOK THEN
            bAlarmCritical := TRUE;
        END_IF;

    10: (* STATE 10: INITIALIZATION & FILLING *)
        bSystemReady := FALSE;
        
        (* Open fresh water until conductivity drops (indicating dilution of old highly concentrated liquor) *)
        IF rFiltered_Conductivity > 2500.0 THEN
            bFreshWaterValveOpen := TRUE;
            bRecoveryPumpRun := FALSE;
        ELSE
            bFreshWaterValveOpen := FALSE;
            bRecoveryPumpRun := TRUE; (* Start recirculating recovery water *)
        END_IF;

        tInitializationTimer(IN := TRUE, PT := T#30S);
        IF tInitializationTimer.Q THEN
            tInitializationTimer(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* STATE 20: HEATING & TEMPERATURE STABILIZATION *)
        (* PID Control for Steam Valve - P+I Action *)
        rTemp_Error := c_Temp_Setpoint - rTunnelTempZone1;
        rTemp_Integral := rTemp_Integral + rTemp_Error * 0.1; (* Simulated execution time scaling *)
        
        (* Anti-windup for Temperature Integral *)
        IF rTemp_Integral > 100.0 THEN rTemp_Integral := 100.0; END_IF;
        IF rTemp_Integral < 0.0 THEN rTemp_Integral := 0.0; END_IF;
        
        rHeatingValvePosition := (c_Kp_Temp * rTemp_Error) + (c_Ki_Temp * rTemp_Integral);
        
        (* Clamp valve position *)
        IF rHeatingValvePosition > 100.0 THEN rHeatingValvePosition := 100.0; END_IF;
        IF rHeatingValvePosition < 0.0 THEN rHeatingValvePosition := 0.0; END_IF;

        tTempStabilization(IN := (rTunnelTempZone1 >= c_Temp_Setpoint - 2.0), PT := T#15S);
        IF tTempStabilization.Q THEN
            iState := 30;
        END_IF;

        IF NOT bSystemEnable THEN iState := 0; END_IF;

    30: (* STATE 30: ACTIVE WASH & CHEMICAL DOSING *)
        bSystemReady := TRUE;
        
        (* Only perform active dosing when linen is not transferring *)
        IF NOT bLinenTransferActive THEN
            (* PID Control for Alkali Dosing to maintain pH *)
            rpH_Error := c_pH_Setpoint - rFiltered_pH;
            
            (* Only integrate if error is significant to prevent dosing wind-up on small fluctuations *)
            IF ABS(rpH_Error) > 0.2 THEN
                rpH_Integral := rpH_Integral + rpH_Error * 0.1;
            END_IF;
            
            (* Anti-windup limits for chemical dosing *)
            IF rpH_Integral > 50.0 THEN rpH_Integral := 50.0; END_IF;
            IF rpH_Integral < 0.0 THEN rpH_Integral := 0.0; END_IF;
            
            (* Proportional-Integral-Derivative equation for pH dosing pump *)
            rAlkaliDosingPumpSpeed := (c_Kp_pH * rpH_Error) + (c_Ki_pH * rpH_Integral) - (5.0 * rDerivativepH);
            
            (* Clamp dosing speeds *)
            IF rAlkaliDosingPumpSpeed > 100.0 THEN rAlkaliDosingPumpSpeed := 100.0; END_IF;
            IF rAlkaliDosingPumpSpeed < 0.0 THEN rAlkaliDosingPumpSpeed := 0.0; END_IF;
            
            (* Base detergent dosing as a ratio of inlet flow *)
            rDetergentDosingPumpSpeed := rInletWaterFlow * 0.5;
            IF rDetergentDosingPumpSpeed > 100.0 THEN rDetergentDosingPumpSpeed := 100.0; END_IF;
            
        ELSE
            (* Stop chemical dosing during actual tunnel transfer pulse to avoid local concentration peaks *)
            rAlkaliDosingPumpSpeed := 0.0;
            rDetergentDosingPumpSpeed := 0.0;
        END_IF;
        
        (* Quality Monitoring *)
        bWarningQuality := (rFiltered_pH < c_pH_Setpoint - 1.0) OR (rTunnelTempZone1 < c_Temp_Setpoint - 5.0);
        
        IF NOT bSystemEnable THEN
            iState := 0;
            bSystemReady := FALSE;
        END_IF;

    999: (* STATE 999: FAULT HANDLING *)
        bSystemReady := FALSE;
        rAlkaliDosingPumpSpeed := 0.0;
        rDetergentDosingPumpSpeed := 0.0;
        rHeatingValvePosition := 0.0;
        bFreshWaterValveOpen := FALSE;
        bRecoveryPumpRun := FALSE;
        
        (* Fault reset mechanism *)
        IF NOT bAlarmCritical AND bSystemEnable THEN
            iState := 0;
        END_IF;

END_CASE;

(* Update current state for external visualization *)
iCurrentState := iState;

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
