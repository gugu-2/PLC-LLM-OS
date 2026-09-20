import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V4 Persona: a 50+ years experienced Chief PLC Architect & Control Systems PhD. 
Your logic must include advanced Non-Linear PID with Anti-Windup, 3-level cascade control, digital low-pass filtering, predictive anomaly detection, and multi-layered hardware interlocks. Output the most elite, mathematically rigorous, and structurally flawless IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial High-Speed Lithium-Ion Battery Slurry Coating Slot Die Gap and Web Tension**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_LiIonCoating_SlotDieWeb\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
   record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
   with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
       json.dump(record, f, ensure_ascii=False)
5. SELF-CHECK before saving - verify ALL:
   [ ] Fence is ```iec-st
   [ ] First code line: FUNCTION_BLOCK FB_<name>
   [ ] Has VAR_INPUT & VAR_OUTPUT sections
   [ ] Has END_IF; or END_CASE;
   [ ] Last code line: END_FUNCTION_BLOCK
   [ ] Closing fence: ```
   [ ] Total chars >= 2000
6. REPLY with: EVOLUTION COMPLETE: Industrial High-Speed Lithium-Ion Battery Slurry Coating Slot Die Gap and Web Tension"""

code = """```iec-st
FUNCTION_BLOCK FB_LiIonCoating_SlotDieWeb
VAR_INPUT
    (* Mandatory Hardware Safety Interlocks *)
    bEnable                 : BOOL;     (* System master enable signal *)
    bEmergencyStop          : BOOL;     (* Main software E-Stop / Safety relay OK signal *)
    bEStopHW_TensionZone    : BOOL;     (* Hardware E-Stop for Web Tension zone *)
    bEStopHW_CoatingZone    : BOOL;     (* Hardware E-Stop for Slot Die Coating zone *)

    (* Process Variables (Sensors) *)
    rWebTensionAct_N        : REAL;     (* Actual web tension from load cells [Newtons] *)
    rSlotDieGapAct_um       : REAL;     (* Actual slot die gap measured via laser [micrometers] *)
    rLineSpeedAct_mpm       : REAL;     (* Actual line speed [meters per minute] *)
    rSlurryViscosity_cP     : REAL;     (* Inline slurry viscosity [Centipoise] *)
    rSlurryPressure_bar     : REAL;     (* Slurry delivery pressure at slot die head [Bar] *)
    
    (* Setpoints *)
    rWebTensionSP_N         : REAL := 150.0; (* Web tension setpoint [Newtons] *)
    rSlotDieGapSP_um        : REAL := 45.0;  (* Coating gap setpoint [micrometers] *)
END_VAR
VAR_OUTPUT
    (* Status & Alarms *)
    bSystemReady            : BOOL;     (* System is ready for coating *)
    bCoatingActive          : BOOL;     (* Coating process is actively running *)
    bAnomalyDetected        : BOOL;     (* Predictive anomaly detection flag *)
    bCriticalAlarm          : BOOL;     (* Fault / Critical alarm output *)
    bWarningAlarm           : BOOL;     (* Warning level alarm *)

    (* Actuator Commands *)
    rTensionMotorCmd_Torque : REAL;     (* Command to tensioning servo motor [% Torque] *)
    rGapActuatorCmd_um      : REAL;     (* Command to piezo gap actuators [micrometers] *)
    rPumpSpeedCmd_rpm       : REAL;     (* Command to slurry delivery pump [RPM] *)
END_VAR
VAR
    (* Internal State Machine *)
    iState                  : INT := 0;
    
    (* Timers *)
    tStartupDelay           : TON;
    tTensionStabilize       : TON;
    tAnomalyFilter          : TON;
    
    (* Digital Low-Pass Filter Variables *)
    rFilteredTension        : REAL := 0.0;
    rFilteredGap            : REAL := 0.0;
    rAlpha                  : REAL := 0.15; (* Filter coefficient *)
    
    (* Non-Linear PID Variables for Gap Control *)
    rGapError               : REAL;
    rGapErrorPrev           : REAL := 0.0;
    rGapIntegral            : REAL := 0.0;
    rGapDerivative          : REAL;
    rKp                     : REAL := 1.2;
    rKi                     : REAL := 0.05;
    rKd                     : REAL := 0.1;
    rNonLinearGain          : REAL;
    rAntiWindupLimit        : REAL := 50.0;
    
    (* Predictive Anomaly Detection *)
    rPressureDelta          : REAL;
    rPressurePrev           : REAL := 0.0;
    rPressureRateLimit      : REAL := 0.5; (* Max bar/sec allowed *)
    
    (* Cascade Control Variables *)
    rBasePumpSpeed          : REAL;
    rViscosityComp          : REAL;
END_VAR

(* === MAIN LOGIC === *)
(* 1. Multi-layered Hardware and Software Interlocks *)
IF NOT bEmergencyStop OR NOT bEStopHW_TensionZone OR NOT bEStopHW_CoatingZone THEN
    bSystemReady := FALSE;
    bCoatingActive := FALSE;
    bCriticalAlarm := TRUE;
    iState := 999; (* FAULT STATE *)
    rTensionMotorCmd_Torque := 0.0;
    rGapActuatorCmd_um := rSlotDieGapAct_um; (* Freeze gap *)
    rPumpSpeedCmd_rpm := 0.0;
    RETURN;
END_IF;

(* 2. Digital Low-Pass Filtering for Noisy Sensor Data *)
rFilteredTension := (rAlpha * rWebTensionAct_N) + ((1.0 - rAlpha) * rFilteredTension);
rFilteredGap := (rAlpha * rSlotDieGapAct_um) + ((1.0 - rAlpha) * rFilteredGap);

(* 3. Predictive Anomaly Detection (Pressure Surge Analysis) *)
rPressureDelta := ABS(rSlurryPressure_bar - rPressurePrev);
rPressurePrev := rSlurryPressure_bar;

IF rPressureDelta > rPressureRateLimit THEN
    tAnomalyFilter(IN := TRUE, PT := T#50MS);
    IF tAnomalyFilter.Q THEN
        bAnomalyDetected := TRUE;
        bWarningAlarm := TRUE;
    END_IF;
ELSE
    tAnomalyFilter(IN := FALSE);
    bAnomalyDetected := FALSE;
END_IF;

(* 4. Main State Machine *)
CASE iState OF
    0: (* IDLE *)
        bSystemReady := FALSE;
        bCoatingActive := FALSE;
        bCriticalAlarm := FALSE;
        rGapActuatorCmd_um := 100.0; (* Retract gap for safety *)
        rPumpSpeedCmd_rpm := 0.0;
        
        IF bEnable THEN
            iState := 10;
        END_IF;

    10: (* INITIALIZATION & TENSION CONTROL *)
        bSystemReady := TRUE;
        (* Simple P-control for startup tension *)
        rTensionMotorCmd_Torque := (rWebTensionSP_N - rFilteredTension) * 0.5;
        
        tTensionStabilize(IN := ABS(rWebTensionSP_N - rFilteredTension) < 5.0, PT := T#2S);
        IF tTensionStabilize.Q THEN
            tTensionStabilize(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* COATING PREPARATION (Gap Approach) *)
        rGapActuatorCmd_um := rSlotDieGapSP_um + 10.0; (* Approach gap safely *)
        tStartupDelay(IN := TRUE, PT := T#1S);
        IF tStartupDelay.Q THEN
            tStartupDelay(IN := FALSE);
            iState := 30;
        END_IF;

    30: (* ACTIVE COATING - Cascade & Non-Linear PID *)
        bCoatingActive := TRUE;
        
        (* Non-Linear PID for Die Gap Control *)
        rGapError := rSlotDieGapSP_um - rFilteredGap;
        
        (* Non-Linear Gain: aggressive for large errors, smooth for small *)
        IF ABS(rGapError) > 5.0 THEN
            rNonLinearGain := 1.5;
        ELSE
            rNonLinearGain := 0.8;
        END_IF;
        
        (* Anti-Windup Integral *)
        rGapIntegral := rGapIntegral + (rGapError * 0.01);
        IF rGapIntegral > rAntiWindupLimit THEN rGapIntegral := rAntiWindupLimit; END_IF;
        IF rGapIntegral < -rAntiWindupLimit THEN rGapIntegral := -rAntiWindupLimit; END_IF;
        
        rGapDerivative := (rGapError - rGapErrorPrev) / 0.01;
        rGapErrorPrev := rGapError;
        
        rGapActuatorCmd_um := (rKp * rNonLinearGain * rGapError) + (rKi * rGapIntegral) + (rKd * rGapDerivative) + rSlotDieGapSP_um;
        
        (* Cascade Control: Pump Speed based on Line Speed, Gap, and Viscosity *)
        rBasePumpSpeed := rLineSpeedAct_mpm * (rSlotDieGapSP_um / 1000.0) * 2.5;
        rViscosityComp := rSlurryViscosity_cP * 0.02; (* Compensate for shear-thinning *)
        
        rPumpSpeedCmd_rpm := rBasePumpSpeed + rViscosityComp;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;
        
    999: (* FAULT / EMERGENCY STATE *)
        bCriticalAlarm := TRUE;
        IF bEnable = FALSE AND bEmergencyStop = TRUE AND bEStopHW_TensionZone = TRUE AND bEStopHW_CoatingZone = TRUE THEN
            iState := 0; (* Reset only if enable dropped and faults cleared *)
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
