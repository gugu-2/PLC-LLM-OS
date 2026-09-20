import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V4 Persona: a 50+ years experienced Chief PLC Architect & Control Systems PhD. 
Your logic must include advanced Non-Linear PID with Anti-Windup, 3-level cascade control, digital low-pass filtering, predictive anomaly detection, and multi-layered hardware interlocks. Output the most elite, mathematically rigorous, and structurally flawless IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Mega-Scale Space Launch Vehicle Friction Stir Welding (FSW) Gantry Downforce and Tool Rotation Sync**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_AeroFSW_WeldingControl\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Mega-Scale Space Launch Vehicle Friction Stir Welding (FSW) Gantry Downforce and Tool Rotation Sync"""

code = """```iec-st
FUNCTION_BLOCK FB_AeroFSW_WeldingSyncControl
VAR_INPUT
    (* Safety and Master Enable Signals *)
    bSystemEnable      : BOOL; (* Master system enable for FSW operations *)
    bEmergencyStopOk   : BOOL; (* E-Stop chain healthy, normally TRUE *)
    bHardLimitReached  : BOOL; (* Gantry structural hard limit proximity switch *)
    bCoolingSystemOk   : BOOL; (* Main cooling system for spindle motor healthy *)
    bSafetyGuardClosed : BOOL; (* Interlock for operator safety guard *)
    bVacuumHoldDownOk  : BOOL; (* Vacuum clamping system maintaining vacuum *)
    
    (* Process Variables - Measurements *)
    rMeasuredDownforce : REAL; (* Actual measured plunge downforce [kN] *)
    rMeasuredRPM       : REAL; (* Actual tool rotation speed [RPM] *)
    rMaterialTemp      : REAL; (* Real-time weld zone temperature via pyrometer [deg C] *)
    rTraverseSpeed     : REAL; (* Linear traverse speed of the gantry [mm/s] *)
    
    (* Setpoints & Reference Targets *)
    rTargetDownforce   : REAL; (* Desired constant downforce for defect-free weld [kN] *)
    rTargetRPM         : REAL; (* Desired base tool RPM [RPM] *)
    rMaxTempThreshold  : REAL; (* Upper thermal threshold for localized melting prevention [deg C] *)
END_VAR
VAR_OUTPUT
    (* Status and Alarms *)
    bSystemReady       : BOOL; (* All interlocks met, ready for welding sequence *)
    bWeldingActive     : BOOL; (* Welding process currently active and traversing *)
    bCriticalAlarm     : BOOL; (* Safety or process limit breached, immediate halt initiated *)
    bMaintenanceReq    : BOOL; (* Preventive maintenance flag triggered by duty cycle *)
    iAlarmCode         : INT;  (* Diagnostic code for HMI (0=OK, 1..=Errors) *)
    
    (* Actuator Control Signals - Sent to Servo Drives & Hydraulics *)
    rZAxisForceCmd     : REAL; (* Commanded downforce to Z-axis hydraulic/servo unit [kN] *)
    rSpindleSpeedCmd   : REAL; (* Commanded spindle speed to VFD [RPM] *)
    rTraverseSpeedCmd  : REAL; (* Gantry linear X/Y feed rate command [mm/s] *)
END_VAR
VAR
    (* Internal State and Sequence Timers *)
    iState             : INT := 0; 
    tRampUpTimer       : TON;
    tDwellTimer        : TON;
    tCooldownTimer     : TON;
    tFaultTimer        : TON;
    
    (* Advanced Digital Low-Pass Filtering States *)
    rFilteredForce     : REAL := 0.0;
    rFilteredTemp      : REAL := 0.0;
    rFilteredRPM       : REAL := 0.0;
    
    (* Cascade Control Variables & Non-Linear PID with Anti-Windup *)
    rForceError        : REAL;
    rForceIntegral     : REAL := 0.0;
    rForceDerivative   : REAL := 0.0;
    rForceLastError    : REAL := 0.0;
    rForceP_Term       : REAL;
    
    rSpindleError      : REAL;
    
    (* Model-Based Constants & Tuning Parameters *)
    rKp_Force          : REAL := 3.25; (* Adaptive Proportional Gain for Z-Axis *)
    rKi_Force          : REAL := 0.12; (* Integral Gain *)
    rKd_Force          : REAL := 0.08; (* Derivative Gain to suppress oscillations *)
    
    rFilterAlphaForce  : REAL := 0.05; (* EMA coefficient for noisy load cells *)
    rFilterAlphaTemp   : REAL := 0.15; (* EMA coefficient for optical pyrometers *)
    
    rMaxDownforceDelta : REAL := 15.0; (* Max allowable force tracking error [kN] before abort *)
    
    (* Predictive Anomaly Flags *)
    bThermalRunaway    : BOOL := FALSE;
    bStallPredicted    : BOOL := FALSE;
END_VAR

(* === MAIN LOGIC === *)
(* 1. Hardware Interlocks, Multi-Layer Safety & Immediate Halt *)
IF NOT bEmergencyStopOk OR bHardLimitReached OR NOT bSafetyGuardClosed THEN
    bSystemReady := FALSE;
    bWeldingActive := FALSE;
    bCriticalAlarm := TRUE;
    iAlarmCode := 99; (* 99: E-Stop or Critical Safety Interlock Tripped *)
    rZAxisForceCmd := 0.0;
    rSpindleSpeedCmd := 0.0;
    rTraverseSpeedCmd := 0.0;
    iState := 0;
    RETURN;
END_IF;

IF NOT bCoolingSystemOk OR NOT bVacuumHoldDownOk THEN
    bSystemReady := FALSE;
    IF iState > 10 THEN
        bCriticalAlarm := TRUE;
        iAlarmCode := 88; (* 88: Auxilliary system failure during operation *)
        iState := 900; (* Transition to fault abort *)
    END_IF;
END_IF;

(* 2. Advanced Signal Processing & Noise Filtering (Exponential Moving Average) *)
rFilteredForce := (rFilterAlphaForce * rMeasuredDownforce) + ((1.0 - rFilterAlphaForce) * rFilteredForce);
rFilteredTemp  := (rFilterAlphaTemp * rMaterialTemp) + ((1.0 - rFilterAlphaTemp) * rFilteredTemp);
rFilteredRPM   := (0.2 * rMeasuredRPM) + (0.8 * rFilteredRPM);

(* 3. Predictive Anomaly Detection & Envelope Protection *)
bThermalRunaway := (rFilteredTemp > rMaxTempThreshold * 0.95) AND ((rFilteredTemp - rMaterialTemp) > 10.0);
bStallPredicted := (rTargetRPM > 100.0) AND (rFilteredRPM < rTargetRPM * 0.5) AND (rZAxisForceCmd > rTargetDownforce * 0.8);

IF bThermalRunaway THEN
    bCriticalAlarm := TRUE;
    iAlarmCode := 10; (* 10: Predictive Thermal Runaway detected *)
    iState := 900;
END_IF;

IF bStallPredicted THEN
    bCriticalAlarm := TRUE;
    iAlarmCode := 12; (* 12: Tool Stall predicted due to high torque/force and low RPM *)
    iState := 900;
END_IF;

IF ABS(rTargetDownforce - rFilteredForce) > rMaxDownforceDelta AND iState = 30 THEN
    bCriticalAlarm := TRUE;
    iAlarmCode := 11; (* 11: Force tracking loss exceeding physical capabilities *)
    iState := 900;
END_IF;

(* 4. Complex State Machine for FSW Synchronization *)
CASE iState OF
    0: (* INIT / SYSTEM IDLE *)
        bSystemReady := TRUE;
        bWeldingActive := FALSE;
        bCriticalAlarm := FALSE;
        iAlarmCode := 0;
        rZAxisForceCmd := 0.0;
        rSpindleSpeedCmd := 0.0;
        rTraverseSpeedCmd := 0.0;
        
        (* Reset PID States *)
        rForceIntegral := 0.0;
        rForceLastError := 0.0;
        
        IF bSystemEnable THEN
            iState := 10;
        END_IF;

    10: (* ACCELERATION & SPINDLE SPIN-UP (Phase 1) *)
        bSystemReady := FALSE;
        rSpindleSpeedCmd := rTargetRPM;
        
        (* Wait for spindle to achieve steady-state synchronous rotation *)
        tRampUpTimer(IN := TRUE, PT := T#8S);
        IF tRampUpTimer.Q AND (rFilteredRPM >= rTargetRPM * 0.95) THEN
            tRampUpTimer(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* PIN PLUNGE & THERMAL DWELL (Phase 2) *)
        (* Command partial downforce for initial friction generation before plasticization *)
        rZAxisForceCmd := rTargetDownforce * 0.6; 
        
        (* Dwell allows frictional heat to soften aluminum alloys (e.g. 2195 for Space Launch) *)
        tDwellTimer(IN := TRUE, PT := T#12S);
        IF tDwellTimer.Q AND rFilteredForce >= (rTargetDownforce * 0.55) AND rFilteredTemp > 300.0 THEN
            tDwellTimer(IN := FALSE);
            iState := 30;
        END_IF;

    30: (* ACTIVE STEADY-STATE WELDING (Phase 3) *)
        bWeldingActive := TRUE;
        
        (* Non-Linear PID with Anti-Windup for precise Z-Axis Downforce *)
        rForceError := rTargetDownforce - rFilteredForce;
        
        (* Adaptive Proportional Gain: softer response near target, aggressive when deviating *)
        IF ABS(rForceError) < 2.0 THEN
            rForceP_Term := (rKp_Force * 0.5) * rForceError;
        ELSE
            rForceP_Term := rKp_Force * rForceError;
        END_IF;
        
        rForceIntegral := rForceIntegral + (rForceError * 0.01); (* Assuming standard 10ms task cycle *)
        
        (* Anti-Windup Clamping *)
        IF rForceIntegral > 40.0 THEN rForceIntegral := 40.0; END_IF;
        IF rForceIntegral < -40.0 THEN rForceIntegral := -40.0; END_IF;
        
        rForceDerivative := (rForceError - rForceLastError) / 0.01;
        rForceLastError := rForceError;
        
        rZAxisForceCmd := rForceP_Term + (rKi_Force * rForceIntegral) + (rKd_Force * rForceDerivative);
        
        (* Tool Rotation & Traverse Sync based on Thermal Feedback (Cascade Control) *)
        IF rFilteredTemp < (rMaxTempThreshold * 0.7) THEN
            (* Too cold: Increase friction via higher RPM, slow traverse *)
            rSpindleSpeedCmd := rTargetRPM * 1.05; 
            rTraverseSpeedCmd := 5.0; 
        ELSIF rFilteredTemp > (rMaxTempThreshold * 0.9) THEN
            (* Too hot: Reduce friction, maintain traverse *)
            rSpindleSpeedCmd := rTargetRPM * 0.85;
            rTraverseSpeedCmd := 8.0;
        ELSE
            (* Optimal Zone *)
            rSpindleSpeedCmd := rTargetRPM;
            rTraverseSpeedCmd := 7.5; (* Nominal feed rate in mm/s *)
        END_IF;
        
        IF NOT bSystemEnable THEN
            iState := 40;
        END_IF;

    40: (* RETRACTION & CONTROLLED COOLDOWN (Phase 4) *)
        bWeldingActive := FALSE;
        rTraverseSpeedCmd := 0.0; (* Stop lateral movement *)
        rZAxisForceCmd := 0.0;    (* Lift spindle *)
        rSpindleSpeedCmd := rTargetRPM * 0.2; (* Slow rotation during extraction *)
        
        tCooldownTimer(IN := TRUE, PT := T#15S);
        IF tCooldownTimer.Q THEN
            tCooldownTimer(IN := FALSE);
            iState := 0;
        END_IF;

    900: (* EMERGENCY FAULT HANDLING SEQUENCE *)
        bWeldingActive := FALSE;
        rZAxisForceCmd := 0.0; (* Immediate pressure release *)
        rTraverseSpeedCmd := 0.0;
        
        (* Decelerate spindle smoothly to avoid mechanical shearing of the pin *)
        rSpindleSpeedCmd := rFilteredRPM * 0.9; 
        IF rFilteredRPM < 10.0 THEN
            rSpindleSpeedCmd := 0.0;
        END_IF;
        
        (* Fault latched until master enable is cycled *)
        IF NOT bSystemEnable THEN
            bCriticalAlarm := FALSE;
            iAlarmCode := 0;
            iState := 0;
        END_IF;
END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
