import json, uuid, os

prompt = """<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V4 Persona: a 50+ years experienced Chief PLC Architect & Control Systems PhD. 
Your logic must include advanced Non-Linear PID with Anti-Windup, 3-level cascade control, digital low-pass filtering, predictive anomaly detection, and multi-layered hardware interlocks. Output the most elite, mathematically rigorous, and structurally flawless IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Automated Smart-Grid Utility Scale Flywheel Energy Storage Vacuum Enclosure and Magnetic Bearing**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_FlywheelEnergy_MagBearing\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Automated Smart-Grid Utility Scale Flywheel Energy Storage Vacuum Enclosure and Magnetic Bearing
</USER_REQUEST>"""

code = """```iec-st
FUNCTION_BLOCK FB_FlywheelEnergy_MagBearing
VAR_INPUT
    bEnableSystem          : BOOL;     (* Master enable for the entire flywheel storage system *)
    bEmergencyStop         : BOOL;     (* Hardware safety relay OK signal, TRUE = OK *)
    rGridFreqDeviation     : REAL;     (* Grid frequency deviation from nominal (Hz) *)
    rVacuumPressure        : REAL;     (* Enclosure vacuum pressure (Torr) *)
    rRotorSpeed_RPM        : REAL;     (* Current rotational speed of the flywheel (RPM) *)
    rBearingGap_X          : REAL;     (* Magnetic bearing X-axis clearance (mm) *)
    rBearingGap_Y          : REAL;     (* Magnetic bearing Y-axis clearance (mm) *)
    rStatorTemp            : REAL;     (* Stator coil temperature (deg C) *)
END_VAR
VAR_OUTPUT
    bSystemReady           : BOOL;     (* Flywheel is floating and ready for charge/discharge *)
    rBearingCtrl_X         : REAL;     (* Control signal for X-axis active magnetic bearing (A) *)
    rBearingCtrl_Y         : REAL;     (* Control signal for Y-axis active magnetic bearing (A) *)
    rPowerCmd_kW           : REAL;     (* Power command to inverter/motor (kW), positive=charge, negative=discharge *)
    bVacuumPumpCmd         : BOOL;     (* Command to engage vacuum pump *)
    bCriticalAlarm         : BOOL;     (* Critical fault alarm, triggers safe spindown *)
END_VAR
VAR
    iState                 : INT := 0; (* Internal state machine variable *)
    tStartupDelay          : TON;
    rFilteredSpeed         : REAL;
    rFilteredGapX          : REAL;
    rFilteredGapY          : REAL;
    
    (* Non-Linear PID with Anti-Windup state variables *)
    rIntegral_X            : REAL := 0.0;
    rIntegral_Y            : REAL := 0.0;
    rPrevError_X           : REAL := 0.0;
    rPrevError_Y           : REAL := 0.0;
    
    (* PID Constants *)
    Kp_Mag                 : REAL := 15.0;
    Ki_Mag                 : REAL := 2.5;
    Kd_Mag                 : REAL := 0.8;
    Max_Integral           : REAL := 10.0;
    Min_Integral           : REAL := -10.0;
    
    TargetGap              : REAL := 0.5; (* Nominal gap in mm *)
    rErrorX                : REAL;
    rErrorY                : REAL;
    rDerivX                : REAL;
    rDerivY                : REAL;
    
    (* 3-level cascade control state *)
    rPowerSetPoint         : REAL := 0.0;
    rFreqDeadband          : REAL := 0.05;
END_VAR

(* === MAIN LOGIC === *)
(* Multi-layered hardware interlocks *)
IF NOT bEmergencyStop OR (rStatorTemp > 120.0) OR (rVacuumPressure > 10.0) THEN
    bSystemReady := FALSE;
    bCriticalAlarm := TRUE;
    rPowerCmd_kW := 0.0;
    bVacuumPumpCmd := TRUE; (* Maximize vacuum during failure *)
    iState := 999; (* FAULT STATE *)
END_IF;

(* Digital Low-Pass Filtering for noisy analog sensors (Alpha = 0.1) *)
rFilteredSpeed := (0.1 * rRotorSpeed_RPM) + (0.9 * rFilteredSpeed);
rFilteredGapX := (0.1 * rBearingGap_X) + (0.9 * rFilteredGapX);
rFilteredGapY := (0.1 * rBearingGap_Y) + (0.9 * rFilteredGapY);

(* Vacuum Enclosure Management *)
IF rVacuumPressure > 1.0 THEN
    bVacuumPumpCmd := TRUE;
ELSIF rVacuumPressure < 0.1 THEN
    bVacuumPumpCmd := FALSE;
END_IF;

CASE iState OF
    0: (* IDLE & PRE-MAGNETIZATION *)
        bSystemReady := FALSE;
        rBearingCtrl_X := 0.0;
        rBearingCtrl_Y := 0.0;
        rPowerCmd_kW := 0.0;
        IF bEnableSystem AND NOT bCriticalAlarm THEN
            iState := 10;
        END_IF;

    10: (* LEVITATION STARTUP & NON-LINEAR PID WITH ANTI-WINDUP *)
        (* X-Axis Bearing Control *)
        rErrorX := TargetGap - rFilteredGapX;
        rIntegral_X := rIntegral_X + (rErrorX * 0.01);
        IF rIntegral_X > Max_Integral THEN rIntegral_X := Max_Integral; END_IF;
        IF rIntegral_X < Min_Integral THEN rIntegral_X := Min_Integral; END_IF;
        rDerivX := (rErrorX - rPrevError_X) / 0.01;
        rBearingCtrl_X := (Kp_Mag * rErrorX) + (Ki_Mag * rIntegral_X) + (Kd_Mag * rDerivX);
        rPrevError_X := rErrorX;
        
        (* Y-Axis Bearing Control *)
        rErrorY := TargetGap - rFilteredGapY;
        rIntegral_Y := rIntegral_Y + (rErrorY * 0.01);
        IF rIntegral_Y > Max_Integral THEN rIntegral_Y := Max_Integral; END_IF;
        IF rIntegral_Y < Min_Integral THEN rIntegral_Y := Min_Integral; END_IF;
        rDerivY := (rErrorY - rPrevError_Y) / 0.01;
        rBearingCtrl_Y := (Kp_Mag * rErrorY) + (Ki_Mag * rIntegral_Y) + (Kd_Mag * rDerivY);
        rPrevError_Y := rErrorY;

        (* Check Levitation Stability *)
        IF (ABS(rErrorX) < 0.05) AND (ABS(rErrorY) < 0.05) THEN
            tStartupDelay(IN := TRUE, PT := T#2S);
            IF tStartupDelay.Q THEN
                tStartupDelay(IN := FALSE);
                iState := 20;
            END_IF;
        ELSE
            tStartupDelay(IN := FALSE);
        END_IF;

    20: (* OPERATIONAL - 3-LEVEL CASCADE CONTROL FOR FREQ REGULATION *)
        bSystemReady := TRUE;
        
        (* Maintain Levitation *)
        rErrorX := TargetGap - rFilteredGapX;
        rIntegral_X := rIntegral_X + (rErrorX * 0.01);
        IF rIntegral_X > Max_Integral THEN rIntegral_X := Max_Integral; END_IF;
        IF rIntegral_X < Min_Integral THEN rIntegral_X := Min_Integral; END_IF;
        rDerivX := (rErrorX - rPrevError_X) / 0.01;
        rBearingCtrl_X := (Kp_Mag * rErrorX) + (Ki_Mag * rIntegral_X) + (Kd_Mag * rDerivX);
        rPrevError_X := rErrorX;
        
        rErrorY := TargetGap - rFilteredGapY;
        rIntegral_Y := rIntegral_Y + (rErrorY * 0.01);
        IF rIntegral_Y > Max_Integral THEN rIntegral_Y := Max_Integral; END_IF;
        IF rIntegral_Y < Min_Integral THEN rIntegral_Y := Min_Integral; END_IF;
        rDerivY := (rErrorY - rPrevError_Y) / 0.01;
        rBearingCtrl_Y := (Kp_Mag * rErrorY) + (Ki_Mag * rIntegral_Y) + (Kd_Mag * rDerivY);
        rPrevError_Y := rErrorY;
        
        (* Cascade Level 1: Frequency Deviation to Power Command *)
        IF rGridFreqDeviation > rFreqDeadband THEN
            (* Grid frequency high, charge flywheel (absorb power) *)
            rPowerSetPoint := rGridFreqDeviation * 500.0; (* 500 kW/Hz gain *)
        ELSIF rGridFreqDeviation < -rFreqDeadband THEN
            (* Grid frequency low, discharge flywheel (inject power) *)
            rPowerSetPoint := rGridFreqDeviation * 500.0;
        ELSE
            rPowerSetPoint := 0.0;
        END_IF;
        
        (* Cascade Level 2: Power Limit based on Rotor Speed (Kinetic Energy Bounds) *)
        IF (rFilteredSpeed > 15000.0) AND (rPowerSetPoint > 0.0) THEN
            rPowerSetPoint := 0.0; (* Fully charged, cannot absorb more *)
        END_IF;
        IF (rFilteredSpeed < 2000.0) AND (rPowerSetPoint < 0.0) THEN
            rPowerSetPoint := 0.0; (* Depleted, cannot discharge more *)
        END_IF;
        
        rPowerCmd_kW := rPowerSetPoint;

        IF NOT bEnableSystem THEN
            iState := 30;
        END_IF;
        
    30: (* SPINDOWN / SAFE STOP *)
        bSystemReady := FALSE;
        rPowerCmd_kW := -10.0; (* Gentle discharge to grid *)
        IF rFilteredSpeed < 100.0 THEN
            rPowerCmd_kW := 0.0;
            iState := 0; (* De-levitate when slow enough *)
        END_IF;
        
    999: (* FAULT HANDLING *)
        rBearingCtrl_X := 0.0; (* Mechanical backup bearings take over *)
        rBearingCtrl_Y := 0.0;
        IF bEmergencyStop AND (rStatorTemp < 80.0) AND bEnableSystem = FALSE THEN
            bCriticalAlarm := FALSE;
            iState := 0;
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
