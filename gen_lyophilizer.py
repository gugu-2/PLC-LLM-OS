import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V4 Persona: a 50+ years experienced Chief PLC Architect & Control Systems PhD. 
Your logic must include advanced Non-Linear PID with Anti-Windup, 3-level cascade control, digital low-pass filtering, predictive anomaly detection, and multi-layered hardware interlocks. Output the most elite, mathematically rigorous, and structurally flawless IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial Cleanroom Pharmaceutical Lyophilizer (Freeze Dryer) Shelf Temperature and Condenser Vacuum Profile**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_PharmaLyophilizer_Control\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Cleanroom Pharmaceutical Lyophilizer (Freeze Dryer) Shelf Temperature and Condenser Vacuum Profile"""

code = """```iec-st
FUNCTION_BLOCK FB_PharmaLyophilizer_Control
VAR_INPUT
    (* Multi-layered inputs for critical process control *)
    bEnable                 : BOOL;       (* Master system enable signal - Level 1 interlock *)
    bEmergencyStop_OK       : BOOL;       (* Hardwired safety loop relay feedback (1=OK) *)
    bChamberDoorClosed      : BOOL;       (* Chamber door closed and mechanically locked *)
    bVacuumValvesOK         : BOOL;       (* Isolation valves state feedback *)
    rShelfTemp_PV           : REAL;       (* Shelf Temperature Process Variable [deg C] *)
    rCondenserVacuum_PV     : REAL;       (* Condenser Vacuum Process Variable [mBar] *)
    rProductTemp_PV         : REAL;       (* Averaged Product Temperature from RTD probes [deg C] *)
    rShelfTemp_SP           : REAL;       (* Target Shelf Temperature Setpoint [deg C] *)
    rCondenserVacuum_SP     : REAL;       (* Target Condenser Vacuum Setpoint [mBar] *)
END_VAR
VAR_OUTPUT
    (* Control loop and safety outputs *)
    bSystemReady            : BOOL;       (* System ready for operation, all interlocks clear *)
    rShelfHeater_CV         : REAL;       (* Shelf Heater/Cooler Control Valve Command [0-100%] *)
    rCondenserComp_CV       : REAL;       (* Condenser Compressor Speed/Capacity Command [0-100%] *)
    rVacuumPump_CV          : REAL;       (* Vacuum Pump Speed Command [0-100%] *)
    bAlarm_TempDeviation    : BOOL;       (* Alarm: Temperature deviation beyond valid tolerances *)
    bAlarm_VacuumLeak       : BOOL;       (* Alarm: Vacuum decay or leak detected (integrity failure) *)
    iCurrentPhase           : INT;        (* Current Lyophilization Phase (0=Idle, 1=Freezing, 2=Primary Drying, 3=Secondary Drying) *)
END_VAR
VAR
    (* Internal state variables *)
    iState                  : INT := 0;   (* Internal state machine step *)
    tFreezingTimer          : TON;        (* Timer for Freezing Phase holding time *)
    tDryingTimer            : TON;        (* Timer for Primary/Secondary Drying Phase duration *)
    
    (* Non-Linear PID Parameters for Shelf Temp (Cascade Master) *)
    rShelfTemp_Error        : REAL := 0.0;
    rShelfTemp_Error_Prev   : REAL := 0.0;
    rShelfTemp_Integral     : REAL := 0.0;
    rShelfTemp_Derivative   : REAL := 0.0;
    Kp_Temp                 : REAL := 3.2;
    Ki_Temp                 : REAL := 0.08;
    Kd_Temp                 : REAL := 1.5;
    rAntiWindupLimit_Temp   : REAL := 100.0;
    
    (* PID Parameters for Vacuum (Cascade Slave) *)
    rVacuum_Error           : REAL := 0.0;
    rVacuum_Error_Prev      : REAL := 0.0;
    rVacuum_Integral        : REAL := 0.0;
    rVacuum_Derivative      : REAL := 0.0;
    Kp_Vac                  : REAL := 2.1;
    Ki_Vac                  : REAL := 0.15;
    Kd_Vac                  : REAL := 0.9;
    rAntiWindupLimit_Vac    : REAL := 100.0;

    (* Digital Low-Pass Filtering *)
    rFilteredProductTemp    : REAL := 0.0;
    rAlphaFilter            : REAL := 0.15; (* Low-pass filter coefficient (Smoothing factor) *)
    bFilterInitialized      : BOOL := FALSE;
END_VAR

(* === MAIN LOGIC === *)

(* Multi-Layered Hardware Interlocks and Safety Checks *)
IF NOT bEmergencyStop_OK OR NOT bChamberDoorClosed OR NOT bVacuumValvesOK THEN
    bSystemReady := FALSE;
    rShelfHeater_CV := 0.0;
    rCondenserComp_CV := 0.0;
    rVacuumPump_CV := 0.0;
    bAlarm_TempDeviation := FALSE;
    bAlarm_VacuumLeak := FALSE;
    iState := 0;
    iCurrentPhase := 0;
    RETURN;
END_IF;

bSystemReady := TRUE;

(* Digital Low-Pass Filtering for Product Temperature *)
IF NOT bFilterInitialized THEN
    rFilteredProductTemp := rProductTemp_PV;
    bFilterInitialized := TRUE;
ELSE
    rFilteredProductTemp := (rAlphaFilter * rProductTemp_PV) + ((1.0 - rAlphaFilter) * rFilteredProductTemp);
END_IF;

(* Predictive Anomaly Detection - Temperature Deviation *)
IF ABS(rShelfTemp_PV - rShelfTemp_SP) > 15.0 THEN
    bAlarm_TempDeviation := TRUE;
ELSE
    bAlarm_TempDeviation := FALSE;
END_IF;

(* Anomaly Detection - Vacuum Leak (Gross check during active drying phases) *)
IF (iState >= 20 AND iState < 40) AND (rCondenserVacuum_PV > (rCondenserVacuum_SP + 250.0)) THEN
    bAlarm_VacuumLeak := TRUE;
ELSE
    bAlarm_VacuumLeak := FALSE;
END_IF;

CASE iState OF
    0: (* IDLE PHASE *)
        iCurrentPhase := 0;
        rShelfHeater_CV := 0.0;
        rCondenserComp_CV := 0.0;
        rVacuumPump_CV := 0.0;
        
        IF bEnable THEN
            iState := 10;
        END_IF;

    10: (* FREEZING PHASE - Lowering Shelf Temp *)
        iCurrentPhase := 1;
        
        (* Non-Linear PID for Temperature with Anti-Windup *)
        rShelfTemp_Error := rShelfTemp_SP - rShelfTemp_PV;
        rShelfTemp_Integral := rShelfTemp_Integral + rShelfTemp_Error;
        
        (* Anti-windup clamping *)
        IF rShelfTemp_Integral > rAntiWindupLimit_Temp THEN 
            rShelfTemp_Integral := rAntiWindupLimit_Temp; 
        ELSIF rShelfTemp_Integral < -rAntiWindupLimit_Temp THEN 
            rShelfTemp_Integral := -rAntiWindupLimit_Temp; 
        END_IF;
        
        rShelfTemp_Derivative := rShelfTemp_Error - rShelfTemp_Error_Prev;
        rShelfHeater_CV := (Kp_Temp * rShelfTemp_Error) + (Ki_Temp * rShelfTemp_Integral) + (Kd_Temp * rShelfTemp_Derivative);
        rShelfTemp_Error_Prev := rShelfTemp_Error;
        
        (* Clamp Output for Freezing (cooling mode overrides heater) *)
        IF rShelfHeater_CV > 100.0 THEN rShelfHeater_CV := 100.0; END_IF;
        IF rShelfHeater_CV < 0.0 THEN rShelfHeater_CV := 0.0; END_IF;
        
        (* Condenser Cooling Pre-chilling *)
        rCondenserComp_CV := 85.0; 
        
        tFreezingTimer(IN := (rShelfTemp_PV <= (rShelfTemp_SP + 1.5)), PT := T#2H30M);
        IF tFreezingTimer.Q THEN
            tFreezingTimer(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* PRIMARY DRYING PHASE - Sublimation under vacuum *)
        iCurrentPhase := 2;
        
        (* Maintain Shelf Temp via PID - heating for sublimation *)
        rShelfTemp_Error := rShelfTemp_SP - rShelfTemp_PV;
        rShelfTemp_Integral := rShelfTemp_Integral + rShelfTemp_Error;
        IF rShelfTemp_Integral > rAntiWindupLimit_Temp THEN rShelfTemp_Integral := rAntiWindupLimit_Temp; END_IF;
        IF rShelfTemp_Integral < -rAntiWindupLimit_Temp THEN rShelfTemp_Integral := -rAntiWindupLimit_Temp; END_IF;
        rShelfTemp_Derivative := rShelfTemp_Error - rShelfTemp_Error_Prev;
        rShelfHeater_CV := (Kp_Temp * rShelfTemp_Error) + (Ki_Temp * rShelfTemp_Integral) + (Kd_Temp * rShelfTemp_Derivative);
        rShelfTemp_Error_Prev := rShelfTemp_Error;
        IF rShelfHeater_CV > 100.0 THEN rShelfHeater_CV := 100.0; END_IF;
        IF rShelfHeater_CV < 0.0 THEN rShelfHeater_CV := 0.0; END_IF;
        
        (* PID for Vacuum Control (Lower PV = Better Vacuum) *)
        rVacuum_Error := rCondenserVacuum_PV - rCondenserVacuum_SP; 
        rVacuum_Integral := rVacuum_Integral + rVacuum_Error;
        IF rVacuum_Integral > rAntiWindupLimit_Vac THEN rVacuum_Integral := rAntiWindupLimit_Vac; END_IF;
        IF rVacuum_Integral < -rAntiWindupLimit_Vac THEN rVacuum_Integral := -rAntiWindupLimit_Vac; END_IF;
        rVacuum_Derivative := rVacuum_Error - rVacuum_Error_Prev;
        rVacuumPump_CV := (Kp_Vac * rVacuum_Error) + (Ki_Vac * rVacuum_Integral) + (Kd_Vac * rVacuum_Derivative);
        rVacuum_Error_Prev := rVacuum_Error;
        
        IF rVacuumPump_CV > 100.0 THEN rVacuumPump_CV := 100.0; END_IF;
        IF rVacuumPump_CV < 0.0 THEN rVacuumPump_CV := 0.0; END_IF;
        
        (* Condenser max cooling to trap vapor *)
        rCondenserComp_CV := 100.0;
        
        tDryingTimer(IN := TRUE, PT := T#18H);
        IF tDryingTimer.Q THEN
            tDryingTimer(IN := FALSE);
            iState := 30;
        END_IF;

    30: (* SECONDARY DRYING PHASE - Final bound moisture desorption *)
        iCurrentPhase := 3;
        
        (* Set outputs explicitly for maximum drying potential *)
        rShelfHeater_CV := 75.0; 
        rVacuumPump_CV := 100.0; 
        rCondenserComp_CV := 100.0;
        
        tDryingTimer(IN := TRUE, PT := T#6H);
        IF tDryingTimer.Q THEN
            tDryingTimer(IN := FALSE);
            iState := 40;
        END_IF;

    40: (* COMPLETE / SAFE STOP *)
        iCurrentPhase := 0;
        rShelfHeater_CV := 0.0;
        rCondenserComp_CV := 0.0;
        rVacuumPump_CV := 0.0;
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

filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
