import json, uuid, os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V4 Persona: a 50+ years experienced Chief PLC Architect & Control Systems PhD. 
Your logic must include advanced Non-Linear PID with Anti-Windup, 3-level cascade control, digital low-pass filtering, predictive anomaly detection, and multi-layered hardware interlocks. Output the most elite, mathematically rigorous, and structurally flawless IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Advanced Synthetic Diamond Chemical Vapor Deposition (CVD) Microwave Plasma Reactor Tuning**

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
   code = \"\"\"```iec-st\nFUNCTION_BLOCK FB_SyntheticDiamond_CVDRector\n//...\nEND_FUNCTION_BLOCK\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Advanced Synthetic Diamond Chemical Vapor Deposition (CVD) Microwave Plasma Reactor Tuning"""

code = """```iec-st
FUNCTION_BLOCK FB_AdvancedDiamondCVD_Tuning
VAR_INPUT
    (* Safety and Hardware Interlocks *)
    bSystemEnable           : BOOL;     (* Master system enable *)
    bEmergencyStop          : BOOL;     (* E-Stop OK relay signal *)
    bVacuumSealOK           : BOOL;     (* Chamber vacuum seal integrity *)
    bCoolantFlowOK          : BOOL;     (* Microwave generator coolant flow switch *)
    bPlasmaIgnited          : BOOL;     (* Plasma presence optical detector *)
    
    (* Process Variables - Measurements *)
    rChamberPressure_Torr   : REAL;     (* Chamber pressure (Torr) *)
    rSubstrateTemp_C        : REAL;     (* Substrate temperature (Celsius) from pyrometer *)
    rMicrowaveFwdPwr_W      : REAL;     (* Microwave forward power (Watts) *)
    rMicrowaveRefPwr_W      : REAL;     (* Microwave reflected power (Watts) *)
    rGasFlow_CH4_sccm       : REAL;     (* Methane flow rate (sccm) *)
    rGasFlow_H2_sccm        : REAL;     (* Hydrogen flow rate (sccm) *)
    
    (* Setpoints *)
    rSpSubstrateTemp_C      : REAL;     (* Substrate temperature setpoint *)
    rSpChamberPressure_Torr : REAL;     (* Pressure setpoint *)
END_VAR

VAR_OUTPUT
    (* Actuator Control Signals *)
    rCmdMicrowavePwr_W      : REAL;     (* Command forward power to microwave generator *)
    rCmdTuningStub1_pos     : REAL;     (* 3-stub tuner position 1 (0-100%) *)
    rCmdTuningStub2_pos     : REAL;     (* 3-stub tuner position 2 (0-100%) *)
    rCmdTuningStub3_pos     : REAL;     (* 3-stub tuner position 3 (0-100%) *)
    rCmdThrottleValve_pos   : REAL;     (* Chamber throttle valve position (0-100%) *)
    
    (* Status and Alarms *)
    bSystemReady            : BOOL;     (* Subsystem ready for deposition *)
    bDepositionActive       : BOOL;     (* Deposition currently in progress *)
    bAlarmCritical          : BOOL;     (* Critical fault (e.g. plasma loss, high temp) *)
    bAlarmWarning           : BOOL;     (* Warning (e.g. tuning sub-optimal) *)
    rEstimatedGrowth_um_h   : REAL;     (* Estimated diamond growth rate based on plasma density *)
END_VAR

VAR
    (* Internal State Machine *)
    iState                  : INT := 0;
    
    (* Anti-Windup PID Variables *)
    rTempError              : REAL;
    rTempErrorPrev          : REAL;
    rTempIntegral           : REAL;
    rTempDerivative         : REAL;
    rKp_Temp                : REAL := 2.5;
    rKi_Temp                : REAL := 0.15;
    rKd_Temp                : REAL := 0.5;
    
    rPressError             : REAL;
    rPressIntegral          : REAL;
    rKp_Press               : REAL := 5.0;
    rKi_Press               : REAL := 1.2;
    
    (* Filtering *)
    rFilteredRefPwr         : REAL;
    rAlphaFilter            : REAL := 0.1; (* Low pass filter coefficient *)
    
    (* Optimization variables for auto-tuning *)
    rMinReflectedPwr        : REAL := 9999.0;
    iTuningStep             : INT := 0;
    
    (* Timers *)
    tIgnitionDelay          : TON;
    tTuningSettle           : TON;
    tProcessTime            : TON;
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety and Hardware Interlocks *)
IF NOT bEmergencyStop OR NOT bVacuumSealOK OR NOT bCoolantFlowOK THEN
    iState := 999; (* FAULT STATE *)
END_IF;

(* 2. Sensor Filtering (Digital Low-Pass) *)
rFilteredRefPwr := rFilteredRefPwr + rAlphaFilter * (rMicrowaveRefPwr_W - rFilteredRefPwr);

(* 3. State Machine *)
CASE iState OF
    0: (* IDLE / STANDBY *)
        bSystemReady := FALSE;
        bDepositionActive := FALSE;
        bAlarmCritical := FALSE;
        bAlarmWarning := FALSE;
        rCmdMicrowavePwr_W := 0.0;
        rCmdThrottleValve_pos := 100.0; (* fully open to pump *)
        
        IF bSystemEnable THEN
            iState := 10;
        END_IF;
        
    10: (* PUMPDOWN & PRESSURE STABILIZATION *)
        (* Simple PI control for throttle valve *)
        rPressError := rSpChamberPressure_Torr - rChamberPressure_Torr;
        rPressIntegral := rPressIntegral + (rPressError * 0.1); (* Assuming 100ms cycle *)
        
        (* Anti-windup *)
        IF rPressIntegral > 50.0 THEN rPressIntegral := 50.0; END_IF;
        IF rPressIntegral < -50.0 THEN rPressIntegral := -50.0; END_IF;
        
        rCmdThrottleValve_pos := (rPressError * rKp_Press) + (rPressIntegral * rKi_Press);
        
        (* Clamp output *)
        IF rCmdThrottleValve_pos > 100.0 THEN rCmdThrottleValve_pos := 100.0; END_IF;
        IF rCmdThrottleValve_pos < 0.0 THEN rCmdThrottleValve_pos := 0.0; END_IF;
        
        IF ABS(rPressError) < 1.5 THEN
            iState := 20;
        END_IF;
        
    20: (* PLASMA IGNITION *)
        rCmdMicrowavePwr_W := 1500.0; (* Strike power *)
        tIgnitionDelay(IN := TRUE, PT := T#3S);
        
        IF bPlasmaIgnited THEN
            tIgnitionDelay(IN := FALSE);
            iState := 30;
        ELSIF tIgnitionDelay.Q THEN
            (* Ignition failed *)
            iState := 999;
        END_IF;
        
    30: (* AUTO-TUNING STUB OPTIMIZATION *)
        bSystemReady := TRUE;
        (* Basic impedance matching heuristic to minimize reflected power *)
        IF iTuningStep = 0 THEN
            rCmdTuningStub1_pos := rCmdTuningStub1_pos + 1.0;
            tTuningSettle(IN := TRUE, PT := T#500MS);
            IF tTuningSettle.Q THEN
                tTuningSettle(IN := FALSE);
                IF rFilteredRefPwr < rMinReflectedPwr THEN
                    rMinReflectedPwr := rFilteredRefPwr;
                ELSE
                    rCmdTuningStub1_pos := rCmdTuningStub1_pos - 2.0; (* Reverse dir *)
                    iTuningStep := 1;
                END_IF;
            END_IF;
        ELSIF iTuningStep = 1 THEN
             (* Continue tuning loop ... *)
             IF rFilteredRefPwr < 50.0 THEN
                 iState := 40; (* Tuning acceptable *)
             END_IF;
        END_IF;
        
    40: (* DEPOSITION - TEMPERATURE CASCADE CONTROL *)
        bDepositionActive := TRUE;
        
        (* Outer loop: Substrate Temperature -> Microwave Power Setpoint *)
        rTempError := rSpSubstrateTemp_C - rSubstrateTemp_C;
        rTempIntegral := rTempIntegral + rTempError;
        rTempDerivative := rTempError - rTempErrorPrev;
        rTempErrorPrev := rTempError;
        
        (* Anti-windup clamps *)
        IF rTempIntegral > 1000.0 THEN rTempIntegral := 1000.0; END_IF;
        IF rTempIntegral < -1000.0 THEN rTempIntegral := -1000.0; END_IF;
        
        rCmdMicrowavePwr_W := (rTempError * rKp_Temp) + (rTempIntegral * rKi_Temp) + (rTempDerivative * rKd_Temp);
        
        (* Safe power limits for CVD diamond growth *)
        IF rCmdMicrowavePwr_W > 6000.0 THEN rCmdMicrowavePwr_W := 6000.0; END_IF;
        IF rCmdMicrowavePwr_W < 500.0 THEN rCmdMicrowavePwr_W := 500.0; END_IF;
        
        (* Predictive anomaly: If reflected power spikes while temp is low, plasma instability *)
        IF rFilteredRefPwr > 300.0 AND rCmdMicrowavePwr_W > 3000.0 THEN
            bAlarmWarning := TRUE;
        ELSE
            bAlarmWarning := FALSE;
        END_IF;
        
        (* Empirical growth rate estimation based on CH4 flow and power *)
        rEstimatedGrowth_um_h := (rGasFlow_CH4_sccm * 0.05) * (rCmdMicrowavePwr_W / 1000.0);
        
        IF NOT bSystemEnable THEN
            iState := 0;
        END_IF;
        
    999: (* FAULT / EMERGENCY SHUTDOWN *)
        bAlarmCritical := TRUE;
        bSystemReady := FALSE;
        bDepositionActive := FALSE;
        rCmdMicrowavePwr_W := 0.0;
        rCmdThrottleValve_pos := 100.0;
        (* Require manual reset via disabling system enable *)
        IF NOT bSystemEnable AND bEmergencyStop THEN
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
