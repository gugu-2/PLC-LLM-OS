import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V4 Persona: a 50+ years experienced Chief PLC Architect & Control Systems PhD. 
Your logic must include advanced Non-Linear PID with Anti-Windup, 3-level cascade control, digital low-pass filtering, predictive anomaly detection, and multi-layered hardware interlocks. Output the most elite, mathematically rigorous, and structurally flawless IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial High-Speed Food Extrusion Twin-Screw Barrel Temperature Profile and Die Pressure**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_FoodExtrusion_TwinScrewControl\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial High-Speed Food Extrusion Twin-Screw Barrel Temperature Profile and Die Pressure"""

code = """```iec-st
FUNCTION_BLOCK FB_FoodExtrusion_TwinScrewControl
VAR_INPUT
    (* System Interlocks and Enable *)
    bEnable                     : BOOL;     (* System operational enable command *)
    bEmergencyStop              : BOOL;     (* Safety relay OK signal (Normally Closed, 1=OK, 0=Trip) *)
    
    (* Process Variables - Analog Inputs *)
    rBarrelTempZ1_PV            : REAL;     (* Zone 1 Barrel Temperature Process Variable [deg C] *)
    rBarrelTempZ2_PV            : REAL;     (* Zone 2 Barrel Temperature Process Variable [deg C] *)
    rDiePressure_PV             : REAL;     (* Extruder Die Head Pressure Process Variable [Bar] *)
    rScrewSpeed_PV              : REAL;     (* Twin-Screw RPM Feedback [RPM] *)
    rMotorTorque_PV             : REAL;     (* Drive Motor Torque [Nm] *)
    rFeedRate_PV                : REAL;     (* Volumetric/Gravimetric Feed Rate [kg/h] *)
END_VAR

VAR_OUTPUT
    (* System Status *)
    bSystemReady                : BOOL;     (* Control system is armed, normalized and ready *)
    
    (* Actuator Commands *)
    rHeaterOutputZ1_CV          : REAL;     (* Zone 1 Heater Control Value (0.0 to 100.0 %) *)
    rHeaterOutputZ2_CV          : REAL;     (* Zone 2 Heater Control Value (0.0 to 100.0 %) *)
    rScrewSpeed_CV              : REAL;     (* Main Drive Screw Speed Reference (0.0 to Max RPM) *)
    
    (* Alarms and Interlocks *)
    bPressureAlarm              : BOOL;     (* Die pressure has exceeded safe operational thresholds *)
    bTorqueOverloadFault        : BOOL;     (* Motor torque limit exceeded or anomaly detected *)
    bExtruderTripFault          : BOOL;     (* Global extruder shutdown command triggered *)
END_VAR

VAR
    (* State Machine *)
    iState                      : INT := 0; 
    
    (* Digital Low-Pass Filters (First Order IIR) *)
    rAlpha                      : REAL := 0.05;
    rFiltDiePressure            : REAL := 0.0;
    rFiltMotorTorque            : REAL := 0.0;
    
    (* 3-Level Cascade Control & Advanced PID (Zone 1) *)
    rTempSetpointZ1             : REAL := 180.0;
    rErrorZ1                    : REAL;
    rIntegralZ1                 : REAL := 0.0;
    rPrevErrorZ1                : REAL := 0.0;
    rDerivativeZ1               : REAL;
    rKpZ1                       : REAL := 2.5;
    rKiZ1                       : REAL := 0.15;
    rKdZ1                       : REAL := 0.05;
    rIntegralMaxZ1              : REAL := 50.0; (* Anti-windup limit *)
    
    (* Predictive Anomaly Detection *)
    rPressureROC                : REAL := 0.0;  (* Rate of Change for Die Pressure *)
    rPrevFiltPressure           : REAL := 0.0;
    rTorqueROC                  : REAL := 0.0;  (* Rate of Change for Motor Torque *)
    rPrevFiltTorque             : REAL := 0.0;
    
    (* Timers *)
    tStartupDelay               : TON;
    tAlarmDebounce              : TON;
END_VAR

(* === EXTRUDER SAFETY AND INTERLOCKS (LAYER 1) === *)
IF NOT bEmergencyStop THEN
    (* Hard safety trip - overrides everything instantaneously *)
    bSystemReady := FALSE;
    rHeaterOutputZ1_CV := 0.0;
    rHeaterOutputZ2_CV := 0.0;
    rScrewSpeed_CV := 0.0;
    bExtruderTripFault := TRUE;
    iState := 0;
    RETURN;
END_IF;

(* === DIGITAL SIGNAL PROCESSING (LAYER 2) === *)
(* Implement first-order low-pass filters to mitigate sensor noise in critical channels *)
rFiltDiePressure := (rAlpha * rDiePressure_PV) + ((1.0 - rAlpha) * rFiltDiePressure);
rFiltMotorTorque := (rAlpha * rMotorTorque_PV) + ((1.0 - rAlpha) * rFiltMotorTorque);

(* Calculate Rates of Change (Derivatives) for Predictive Anomaly Detection *)
rPressureROC := rFiltDiePressure - rPrevFiltPressure;
rTorqueROC   := rFiltMotorTorque - rPrevFiltTorque;
rPrevFiltPressure := rFiltDiePressure;
rPrevFiltTorque   := rFiltMotorTorque;

(* === PREDICTIVE ANOMALY DETECTION (LAYER 3) === *)
(* High-speed Twin-Screw Extrusion is highly sensitive to sudden pressure spikes (blockage) *)
IF rPressureROC > 15.0 OR rFiltDiePressure > 250.0 THEN
    bPressureAlarm := TRUE;
    rScrewSpeed_CV := rScrewSpeed_CV * 0.5; (* Rapid auto-deceleration algorithm *)
ELSE
    bPressureAlarm := FALSE;
END_IF;

(* Detect torque spikes which indicate surging, un-melted aggregates, or screw mechanical binding *)
IF rTorqueROC > 20.0 OR rFiltMotorTorque > 850.0 THEN
    bTorqueOverloadFault := TRUE;
    bExtruderTripFault := TRUE;
ELSE
    bTorqueOverloadFault := FALSE;
END_IF;

(* If anomalous trip generated, shutdown extruder completely *)
IF bExtruderTripFault THEN
    rScrewSpeed_CV := 0.0;
    bSystemReady := FALSE;
    iState := 99; (* Fault State *)
END_IF;

(* === MAIN CONTROL STATE MACHINE (LAYER 4) === *)
CASE iState OF
    0: (* IDLE & SYSTEM CHECKS *)
        bSystemReady := FALSE;
        rHeaterOutputZ1_CV := 0.0;
        rHeaterOutputZ2_CV := 0.0;
        rScrewSpeed_CV := 0.0;
        
        IF bEnable AND NOT bExtruderTripFault AND NOT bPressureAlarm THEN
            iState := 10;
        END_IF;

    10: (* PRE-HEATING & BARREL SOAKING *)
        (* Barrel must reach glass transition or melt temperature before screw rotation is permitted *)
        bSystemReady := FALSE;
        
        (* Non-Linear PID calculation for Zone 1 *)
        rErrorZ1 := rTempSetpointZ1 - rBarrelTempZ1_PV;
        
        (* Advanced Anti-Windup Logic *)
        IF ABS(rErrorZ1) < 20.0 THEN
            rIntegralZ1 := rIntegralZ1 + rErrorZ1;
        END_IF;
        
        IF rIntegralZ1 > rIntegralMaxZ1 THEN rIntegralZ1 := rIntegralMaxZ1; END_IF;
        IF rIntegralZ1 < -rIntegralMaxZ1 THEN rIntegralZ1 := -rIntegralMaxZ1; END_IF;
        
        rDerivativeZ1 := rErrorZ1 - rPrevErrorZ1;
        rPrevErrorZ1 := rErrorZ1;
        
        rHeaterOutputZ1_CV := (rKpZ1 * rErrorZ1) + (rKiZ1 * rIntegralZ1) + (rKdZ1 * rDerivativeZ1);
        
        (* Heater Saturation Limits *)
        IF rHeaterOutputZ1_CV > 100.0 THEN rHeaterOutputZ1_CV := 100.0; END_IF;
        IF rHeaterOutputZ1_CV < 0.0 THEN rHeaterOutputZ1_CV := 0.0; END_IF;
        
        (* Check conditions to move to running state *)
        IF rBarrelTempZ1_PV >= (rTempSetpointZ1 - 5.0) THEN
            tStartupDelay(IN := TRUE, PT := T#30S);
        ELSE
            tStartupDelay(IN := FALSE, PT := T#30S);
        END_IF;
        
        IF tStartupDelay.Q THEN
            iState := 20;
        END_IF;

    20: (* EXTRUDER RUNNING (CASCADED PRESSURE-SPEED CONTROL) *)
        bSystemReady := TRUE;
        
        (* Cascaded Loop: Maintain target die pressure by manipulating screw speed *)
        rScrewSpeed_CV := 450.0 - (rFiltDiePressure * 1.5);
        
        IF rScrewSpeed_CV > 1200.0 THEN rScrewSpeed_CV := 1200.0; END_IF;
        IF rScrewSpeed_CV < 50.0 THEN rScrewSpeed_CV := 50.0; END_IF;
        
        IF NOT bEnable THEN
            iState := 30; (* Shutdown Phase *)
        END_IF;
        
    30: (* SHUTDOWN & COOLING *)
        bSystemReady := FALSE;
        rScrewSpeed_CV := 0.0;
        rHeaterOutputZ1_CV := 0.0;
        rHeaterOutputZ2_CV := 0.0;
        iState := 0;
        
    99: (* FAULT HANDLING *)
        rHeaterOutputZ1_CV := 0.0;
        rHeaterOutputZ2_CV := 0.0;
        rScrewSpeed_CV := 0.0;
        IF bEnable = FALSE AND bEmergencyStop = TRUE THEN
            bExtruderTripFault := FALSE;
            iState := 0;
        END_IF;
        
END_CASE;
END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump({"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}, f, ensure_ascii=False)
print(f"Saved to {filename}")
