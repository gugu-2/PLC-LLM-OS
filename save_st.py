import os
import json
import uuid

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V4 Persona: a 50+ years experienced Chief PLC Architect & Control Systems PhD. 
Your logic must include advanced Non-Linear PID with Anti-Windup, 3-level cascade control, digital low-pass filtering, predictive anomaly detection, and multi-layered hardware interlocks. Output the most elite, mathematically rigorous, and structurally flawless IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial Wind Tunnel Multi-Stage Axial Fan Pitch and Anti-Surge Stator Vane Control**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_WindTunnel_AxialFanControl\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Wind Tunnel Multi-Stage Axial Fan Pitch and Anti-Surge Stator Vane Control"""

code = """```iec-st
FUNCTION_BLOCK FB_WindTunnel_AxialFanControl
VAR_INPUT
    (* Master System Controls *)
    bEnable                 : BOOL;     (* Master System Enable Signal *)
    bEmergencyStop          : BOOL;     (* Safety Relay Status (1 = OK, 0 = E-Stop active) *)
    
    (* Process Variables - Analog Inputs *)
    rFanSpeedActual         : REAL;     (* Actual Fan Speed from Encoders [RPM] *)
    rFanSpeedSetpoint       : REAL;     (* Desired Fan Speed [RPM] *)
    rAirflowActual          : REAL;     (* Actual Airflow velocity [m/s] measured by Pitot Array *)
    rAirflowSetpoint        : REAL;     (* Desired Airflow velocity [m/s] *)
    rDiffPressureStator     : REAL;     (* Differential Pressure across Stator cascade [Pa] *)
    rStatorVanePosActual    : REAL;     (* Actual Stator Vane Position feedback [Degrees] *)
    rVibrationLevel         : REAL;     (* Bearing Vibration Velocity [mm/s] *)
END_VAR
VAR_OUTPUT
    (* Status & Control Signals *)
    bSystemReady            : BOOL;     (* Drive System Ready to receive commands *)
    rPitchControlCmd        : REAL;     (* Command to Fan Pitch Hydraulic Actuator [Degrees] *)
    rStatorVaneControlCmd   : REAL;     (* Command to Stator Vane Actuator [Degrees] *)
    rMotorTorqueCmd         : REAL;     (* Command to Main VFD for motor torque/speed adjustment [%] *)
    
    (* Alarms and Diagnostics *)
    bSurgeWarning           : BOOL;     (* Warning: Aerodynamic state approaching Surge Line *)
    bAlarmSurgeDetected     : BOOL;     (* Fault: Surge Detected, triggering fast stop *)
    bAlarmVibrationHigh     : BOOL;     (* Fault: Vibration exceeded critical threshold *)
    bAlarmGeneral           : BOOL;     (* General System Fault Flag *)
END_VAR
VAR
    (* Internal State Machine variable *)
    iState                  : INT := 0; 
    
    (* Timers for debouncing and sequencing *)
    tStartupDelay           : TON;      
    tSurgeDebounce          : TON;      
    tVibrationDebounce      : TON;
    
    (* Digital Low-Pass Filters - State Variables *)
    rFilteredAirflow        : REAL := 0.0;
    rFilteredDiffPress      : REAL := 0.0;
    rFilteredVibration      : REAL := 0.0;
    
    (* Non-Linear PID variables - Airflow Loop *)
    rErrorAirflow           : REAL := 0.0;
    rIntAirflow             : REAL := 0.0;
    rDerivAirflow           : REAL := 0.0;
    rPrevErrorAirflow       : REAL := 0.0;
    
    (* Non-Linear PID variables - Speed Loop *)
    rErrorSpeed             : REAL := 0.0;
    rIntSpeed               : REAL := 0.0;
    
    (* PID Constants - Configurable based on operating regime *)
    rKp_Pitch               : REAL := 1.25;
    rKi_Pitch               : REAL := 0.15;
    rKd_Pitch               : REAL := 0.08;
    
    rKp_Speed               : REAL := 2.50;
    rKi_Speed               : REAL := 0.40;
    
    rKp_Stator              : REAL := 1.85; (* Proportional coupling coefficient for stator compensation *)
    
    (* Safety and Hardware Limits *)
    rSurgeThresholdPress    : REAL := 3200.0; (* Max allowable DP before stall/surge [Pa] *)
    rVibrationTripLimit     : REAL := 7.5;    (* Vibration velocity trip threshold [mm/s] *)
    
    rPitchMax               : REAL := 45.0;   (* Max Pitch angle [Degrees] *)
    rPitchMin               : REAL := -15.0;  (* Min Pitch angle [Degrees] (reverse thrust capabilities) *)
    
    rStatorMax              : REAL := 85.0;   (* Max Stator angle [Degrees] (Fully closed / Surge Bypass) *)
    rStatorMin              : REAL := 0.0;    (* Min Stator angle [Degrees] (Wide open) *)
    
    rTorqueMax              : REAL := 100.0;  (* Max allowable motor torque [%] *)
    rTorqueMin              : REAL := 5.0;    (* Min allowable motor torque [%] *)
    
    (* Constants *)
    rAlphaFilter            : REAL := 0.05;   (* Digital Low-Pass Filter Alpha for aggressive smoothing *)
    rDt                     : REAL := 0.01;   (* Task cycle time: 10ms execution time assumed *)
END_VAR

(* === MAIN LOGIC === *)

(* Hardware Interlocks and Safety Chain *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    rPitchControlCmd := 0.0;  (* Safe feathering angle *)
    rStatorVaneControlCmd := rStatorMax; (* Fully open stators / un-load the fan *)
    rMotorTorqueCmd := 0.0;   (* Cut power immediately *)
    bAlarmGeneral := TRUE;
    iState := 0;
    RETURN;
END_IF;

(* Advanced Digital Low-Pass Filtering for all critical analog sensors *)
rFilteredAirflow := (rAlphaFilter * rAirflowActual) + ((1.0 - rAlphaFilter) * rFilteredAirflow);
rFilteredDiffPress := (rAlphaFilter * rDiffPressureStator) + ((1.0 - rAlphaFilter) * rFilteredDiffPress);
rFilteredVibration := (rAlphaFilter * rVibrationLevel) + ((1.0 - rAlphaFilter) * rFilteredVibration);

(* Predictive Anomaly & Surge Detection Logic *)
IF rFilteredDiffPress > (rSurgeThresholdPress * 0.85) THEN
    bSurgeWarning := TRUE;
ELSE
    bSurgeWarning := FALSE;
END_IF;

(* Surge Debounce to prevent spurious trips *)
tSurgeDebounce(IN := (rFilteredDiffPress > rSurgeThresholdPress), PT := T#250MS);
IF tSurgeDebounce.Q THEN
    bAlarmSurgeDetected := TRUE;
    bAlarmGeneral := TRUE;
    iState := 999; (* TRIGGER FAST STOP STATE *)
END_IF;

(* Vibration Monitoring System *)
tVibrationDebounce(IN := (rFilteredVibration > rVibrationTripLimit), PT := T#1S);
IF tVibrationDebounce.Q THEN
    bAlarmVibrationHigh := TRUE;
    bAlarmGeneral := TRUE;
    iState := 999; (* TRIGGER FAST STOP STATE *)
END_IF;

(* Finite State Machine for Multi-Stage Control *)
CASE iState OF
    0: (* IDLE & SAFE STATE *)
        bSystemReady := FALSE;
        rPitchControlCmd := 0.0;
        rStatorVaneControlCmd := rStatorMax;
        rMotorTorqueCmd := 0.0;
        
        (* Anti-windup reset during idle *)
        rIntAirflow := 0.0;
        rIntSpeed := 0.0;
        rPrevErrorAirflow := 0.0;
        
        IF bEnable AND NOT bAlarmGeneral AND NOT bAlarmSurgeDetected AND NOT bAlarmVibrationHigh THEN
            iState := 10;
        END_IF;

    10: (* SYSTEM INITIALIZATION & MAGNETIC FLUX ESTABLISHMENT DELAY *)
        bSystemReady := TRUE;
        tStartupDelay(IN := TRUE, PT := T#5S);
        
        (* Pre-position stators and pitch before torque application *)
        rPitchControlCmd := rPitchMin; 
        rStatorVaneControlCmd := rStatorMax * 0.5;
        
        IF tStartupDelay.Q THEN
            tStartupDelay(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* RUNNING - 3-LEVEL CASCADE CONTROL WITH NON-LINEAR PID *)
        bSystemReady := TRUE;
        
        (* ---------------------------------------------------------
           Cascade Level 1: Outer Loop (Airflow Velocity Control)
           Generates the baseline Pitch Angle setpoint
           --------------------------------------------------------- *)
        rErrorAirflow := rAirflowSetpoint - rFilteredAirflow;
        
        (* Variable Gain Scheduling (Non-linear Kp based on aerodynamic error magnitude) *)
        IF ABS(rErrorAirflow) > 15.0 THEN
            rKp_Pitch := 2.5; (* Aggressive pitch correction during major transients *)
        ELSE
            rKp_Pitch := 1.25; (* Fine tuning near operating point *)
        END_IF;
        
        (* Integral with advanced dynamic Anti-Windup clamping *)
        rIntAirflow := rIntAirflow + (rErrorAirflow * rDt);
        IF rIntAirflow > (rPitchMax / rKi_Pitch) THEN
            rIntAirflow := rPitchMax / rKi_Pitch;
        ELSIF rIntAirflow < (rPitchMin / rKi_Pitch) THEN
            rIntAirflow := rPitchMin / rKi_Pitch;
        END_IF;
        
        (* Derivative term with high-frequency noise rejection implicit via previous LPF *)
        rDerivAirflow := (rErrorAirflow - rPrevErrorAirflow) / rDt;
        rPrevErrorAirflow := rErrorAirflow;
        
        (* Calculate Output for Blade Pitch *)
        rPitchControlCmd := (rKp_Pitch * rErrorAirflow) + (rKi_Pitch * rIntAirflow) + (rKd_Pitch * rDerivAirflow);
        
        (* Enforce Hardware Geometry Limits on Pitch Actuator *)
        IF rPitchControlCmd > rPitchMax THEN
            rPitchControlCmd := rPitchMax;
        ELSIF rPitchControlCmd < rPitchMin THEN
            rPitchControlCmd := rPitchMin;
        END_IF;

        (* ---------------------------------------------------------
           Cascade Level 2: Middle Loop (Motor Speed & Torque Control)
           Compensates for increased aerodynamic drag from pitch changes
           --------------------------------------------------------- *)
        rErrorSpeed := rFanSpeedSetpoint - rFanSpeedActual;
        rIntSpeed := rIntSpeed + (rErrorSpeed * rDt);
        
        (* Speed integral clamping *)
        IF rIntSpeed > (rTorqueMax / rKi_Speed) THEN rIntSpeed := rTorqueMax / rKi_Speed; END_IF;
        IF rIntSpeed < 0.0 THEN rIntSpeed := 0.0; END_IF;
        
        (* Feed-forward torque requirement based on current pitch angle *)
        rMotorTorqueCmd := (rKp_Speed * rErrorSpeed) + (rKi_Speed * rIntSpeed) + (rPitchControlCmd * 0.5);
        
        IF rMotorTorqueCmd > rTorqueMax THEN rMotorTorqueCmd := rTorqueMax; END_IF;
        IF rMotorTorqueCmd < rTorqueMin THEN rMotorTorqueCmd := rTorqueMin; END_IF;

        (* ---------------------------------------------------------
           Cascade Level 3: Inner Loop (Anti-Surge Stator Vane Control)
           Adjusts stator vanes dynamically to maintain optimal 
           incidence angle and strictly prevent compressor stall
           --------------------------------------------------------- *)
        rStatorVaneControlCmd := rStatorMin + (rKp_Stator * (rPitchControlCmd - rPitchMin));
        
        IF bSurgeWarning THEN
            (* Aggressively bypass/dump pressure via stator to avoid crossing the surge line *)
            rStatorVaneControlCmd := rStatorVaneControlCmd + 25.0;
        END_IF;
        
        (* Enforce Hardware Limits on Stator Vanes *)
        IF rStatorVaneControlCmd > rStatorMax THEN
            rStatorVaneControlCmd := rStatorMax;
        ELSIF rStatorVaneControlCmd < rStatorMin THEN
            rStatorVaneControlCmd := rStatorMin;
        END_IF;
        
        (* Orderly Shutdown command received *)
        IF NOT bEnable THEN
            iState := 30;
        END_IF;

    30: (* RAMP DOWN & SAFE SHUTDOWN SEQUENCE *)
        bSystemReady := TRUE;
        rPitchControlCmd := 0.0; (* Feather blades to neutral *)
        rStatorVaneControlCmd := rStatorMax; (* Open stators *)
        rMotorTorqueCmd := rTorqueMin; (* Drop torque to minimum before cutoff *)
        
        IF rFanSpeedActual < 50.0 THEN (* Assuming <50 RPM is safe to cut power *)
            iState := 0;
            tStartupDelay(IN := FALSE);
        END_IF;

    999: (* FAULT / FAST STOP EMERGENCY SEQUENCE *)
        bSystemReady := FALSE;
        
        (* Force equipment to structurally safe orientations immediately *)
        rPitchControlCmd := 0.0; (* Feather blades *)
        rStatorVaneControlCmd := rStatorMax; (* Fully open stators to clear surge/pressure quickly *)
        rMotorTorqueCmd := 0.0; (* Immediate coast-to-stop *)
        
        (* Latch fault state until an explicit reset is given via toggling the enable signal *)
        IF NOT bEnable THEN
            bAlarmSurgeDetected := FALSE;
            bAlarmVibrationHigh := FALSE;
            bAlarmGeneral := FALSE;
            tSurgeDebounce(IN := FALSE);
            tVibrationDebounce(IN := FALSE);
            iState := 0;
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

import os
os.makedirs("data/swarm_raw", exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
