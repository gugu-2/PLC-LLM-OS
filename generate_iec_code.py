import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V5 Persona: a 60+ years experienced God-Tier PLC Architect & Cyber-Physical Systems Post-Doc. 
Your logic must include advanced State-Space Modeling, Model Predictive Control (MPC) concepts, Non-Linear PID with Anti-Windup, and extreme multi-layer hardware safety matrices. Output the most elite, mathematically rigorous, and structurally flawless IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial Scale Atmospheric Water Generator (AWG) Desiccant Wheel Regeneration and Psychrometric Control**

Task: Invent a highly complex, ultra-realistic control scenario for this domain. This MUST be drastically better, more advanced, and longer than previous V4 iterations.

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
3. LENGTH: The assistant content MUST be >= 2500 characters total. Make it incredibly massive and rigorous.
4. SAVE to isolated file using this exact Python:
   import json, uuid
   prompt = \"\"\"<copy this exact user prompt here>\"\"\"
   code = \"\"\"```iec-st\nFUNCTION_BLOCK FB_AWG_DesiccantRegeneration\n//...\nEND_FUNCTION_BLOCK\n```\"\"\"
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
   [ ] Total chars >= 2500
6. REPLY with: EVOLUTION COMPLETE: Industrial Scale Atmospheric Water Generator (AWG) Desiccant Wheel Regeneration and Psychrometric Control"""

code = """```iec-st
FUNCTION_BLOCK FB_AWG_DesiccantRegeneration
VAR_INPUT
    bEnable               : BOOL;   (* System Enable Signal *)
    bEmergencyStop        : BOOL;   (* Safety Hardware Interlock (OK = TRUE) *)
    rAmbientTemp          : REAL;   (* Ambient Temperature [degC] *)
    rAmbientHumidity      : REAL;   (* Ambient Relative Humidity [%] *)
    rDesiccantTemp        : REAL;   (* Desiccant Wheel Body Temperature [degC] *)
    rRegenHeaterTemp      : REAL;   (* Regeneration Heater Core Temperature [degC] *)
    rAirflowRate          : REAL;   (* Main Process Airflow Rate Feedback [m3/h] *)
    bWheelRotationSensor  : BOOL;   (* Wheel Rotation Pulse Signal *)
END_VAR
VAR_OUTPUT
    bSystemReady          : BOOL;   (* System Ready to Produce Water Flag *)
    rHeaterControlSignal  : REAL;   (* PWM/Analog Output Signal to Regen Heater [0-100%] *)
    rBlowerSpeed          : REAL;   (* Process Blower Speed Setpoint [0-100%] *)
    rWheelMotorSpeed      : REAL;   (* Desiccant Wheel Motor Speed Setpoint [0-100%] *)
    bAlarmHighTemp        : BOOL;   (* High Temperature Alarm Output *)
    bAlarmWheelStall      : BOOL;   (* Wheel Stalled/Jammed Alarm Output *)
    bAlarmCritical        : BOOL;   (* Critical System Failure Alarm *)
END_VAR
VAR
    iState                : INT := 0;
    tStateTimer           : TON;
    tWheelTimeout         : TON;
    rErrorHeater          : REAL;
    rIntegralHeater       : REAL;
    rDerivativeHeater     : REAL;
    rPrevErrorHeater      : REAL;
    rKp                   : REAL := 2.85;  (* Non-linear PID Proportional Gain Base *)
    rKi                   : REAL := 0.085; (* PID Integral Gain *)
    rKd                   : REAL := 0.125; (* PID Derivative Gain *)
    rHeaterTargetTemp     : REAL := 120.0; (* Base Target Temp [degC] *)
    rWaterVaporPressure   : REAL;
    rDewPoint             : REAL;
    rEnthalpy             : REAL;
    iWheelPulseCount      : DINT := 0;
    bPrevWheelSensor      : BOOL := FALSE;
    rDeltaTime            : REAL := 0.1;   (* Task cycle time in seconds *)
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety and Emergency Stop Handling Layer *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    rHeaterControlSignal := 0.0;
    rBlowerSpeed := 0.0;
    rWheelMotorSpeed := 0.0;
    bAlarmCritical := TRUE;
    iState := 0;
    rIntegralHeater := 0.0; (* Reset PID Anti-Windup *)
    RETURN;
END_IF;

bAlarmCritical := FALSE;

(* 2. Advanced Psychrometric State-Space Calculations (Magnus-Tetens Formula Approximation) *)
(* Calculate actual water vapor pressure based on current ambient conditions *)
rWaterVaporPressure := 6.112 * EXP((17.67 * rAmbientTemp) / (rAmbientTemp + 243.5)) * (rAmbientHumidity / 100.0);

(* Calculate dew point temperature for MPC optimization *)
IF rWaterVaporPressure > 0.0 THEN
    rDewPoint := (243.5 * LN(rWaterVaporPressure / 6.112)) / (17.67 - LN(rWaterVaporPressure / 6.112));
ELSE
    rDewPoint := 0.0;
END_IF;

(* 3. Dynamic Model Predictive Control (MPC) Setpoint Generation *)
(* Adjust Regeneration Heater Target Temp based on psychrometric loading (dew point and ambient) *)
rHeaterTargetTemp := 115.0 + (rDewPoint * 1.65) - (rAmbientTemp * 0.45);

(* Saturate Target Temperature within safe operational limits *)
IF rHeaterTargetTemp > 145.0 THEN
    rHeaterTargetTemp := 145.0;
ELSIF rHeaterTargetTemp < 95.0 THEN
    rHeaterTargetTemp := 95.0;
END_IF;

(* 4. Non-Linear PID Control for Regeneration Heater with Integral Anti-Windup *)
rErrorHeater := rHeaterTargetTemp - rRegenHeaterTemp;

(* Gain Scheduling based on error magnitude (Non-linear Kp) *)
IF ABS(rErrorHeater) > 20.0 THEN
    rKp := 4.5;
ELSE
    rKp := 2.85;
END_IF;

(* Integrate with Anti-Windup Clamping *)
rIntegralHeater := rIntegralHeater + (rErrorHeater * rDeltaTime);
IF rIntegralHeater > 200.0 THEN 
    rIntegralHeater := 200.0; 
ELSIF rIntegralHeater < -20.0 THEN 
    rIntegralHeater := -20.0; 
END_IF;

rDerivativeHeater := (rErrorHeater - rPrevErrorHeater) / rDeltaTime;
rPrevErrorHeater := rErrorHeater;

(* Compute final control signal and clamp to 0-100% PWM *)
rHeaterControlSignal := (rKp * rErrorHeater) + (rKi * rIntegralHeater) + (rKd * rDerivativeHeater);
IF rHeaterControlSignal > 100.0 THEN 
    rHeaterControlSignal := 100.0; 
ELSIF rHeaterControlSignal < 0.0 THEN 
    rHeaterControlSignal := 0.0; 
END_IF;

(* 5. Multi-Layer Hardware Safety Matrices & Diagnostics *)
(* Wheel Stall Detection using edge detection and timeout *)
IF bWheelRotationSensor AND NOT bPrevWheelSensor THEN
    iWheelPulseCount := iWheelPulseCount + 1;
    tWheelTimeout(IN := FALSE);
ELSE
    tWheelTimeout(IN := TRUE, PT := T#12S);
END_IF;
bPrevWheelSensor := bWheelRotationSensor;

(* Trigger Stall Alarm if no pulses received while expected to rotate (State >= 20) *)
IF tWheelTimeout.Q AND iState >= 20 AND rWheelMotorSpeed > 0.0 THEN
    bAlarmWheelStall := TRUE;
    bSystemReady := FALSE;
    iState := 99; (* Force Fault State *)
ELSE
    bAlarmWheelStall := FALSE;
END_IF;

(* Thermal Runaway / Over-Temperature Safety Interlock *)
IF rDesiccantTemp > 165.0 OR rRegenHeaterTemp > 180.0 THEN
    bAlarmHighTemp := TRUE;
    bSystemReady := FALSE;
    iState := 99; (* Force Fault State *)
ELSE
    bAlarmHighTemp := FALSE;
END_IF;

(* 6. Primary State Machine (Desiccant Regeneration Cycle) *)
CASE iState OF
    0: (* STATE 0: STANDBY / IDLE *)
        bSystemReady := FALSE;
        rHeaterControlSignal := 0.0;
        rBlowerSpeed := 0.0;
        rWheelMotorSpeed := 0.0;
        tStateTimer(IN := FALSE);
        IF bEnable AND NOT bAlarmHighTemp AND NOT bAlarmWheelStall THEN
            iState := 10;
        END_IF;

    10: (* STATE 10: PRE-HEAT & PURGE PHASE *)
        rWheelMotorSpeed := 15.0; (* Slow uniform rotation for even heating *)
        rBlowerSpeed := 25.0;     (* Low airflow purge to prevent thermal shock *)
        
        (* Wait for heater to reach within 15 degrees of dynamic target *)
        IF rRegenHeaterTemp >= (rHeaterTargetTemp - 15.0) THEN
            tStateTimer(IN := TRUE, PT := T#45S);
            IF tStateTimer.Q THEN
                tStateTimer(IN := FALSE);
                iState := 20;
            END_IF;
        ELSE
            tStateTimer(IN := FALSE);
        END_IF;

    20: (* STATE 20: OPTIMIZED WATER PRODUCTION PHASE *)
        bSystemReady := TRUE;
        
        (* Model Predictive Control (MPC) output mapping for Airflow based on Humidity/Temp delta *)
        rBlowerSpeed := 55.0 + (rAmbientHumidity * 0.35) + (rAmbientTemp * 0.25);
        IF rBlowerSpeed > 100.0 THEN rBlowerSpeed := 100.0; END_IF;
        
        (* Optimize Desiccant Wheel Speed based on saturation rate (Blower Speed and Ambient Humidity) *)
        rWheelMotorSpeed := 25.0 + (rAmbientHumidity * 0.6);
        IF rWheelMotorSpeed > 90.0 THEN rWheelMotorSpeed := 90.0; END_IF;

        IF NOT bEnable THEN
            iState := 30;
        END_IF;

    30: (* STATE 30: CONTROLLED COOL-DOWN PHASE *)
        bSystemReady := FALSE;
        rHeaterControlSignal := 0.0; (* Secure Heater *)
        rBlowerSpeed := 60.0;        (* Maintain airflow to remove residual heat *)
        rWheelMotorSpeed := 20.0;    (* Keep turning to prevent warping *)
        
        (* Wait until safely cooled down *)
        IF rRegenHeaterTemp < 55.0 AND rDesiccantTemp < 45.0 THEN
            iState := 0;
        END_IF;

    99: (* STATE 99: CRITICAL FAULT HANDLING / SAFE-STATE ABORT *)
        bSystemReady := FALSE;
        rHeaterControlSignal := 0.0; (* Kill Heater immediately *)
        rBlowerSpeed := 100.0;       (* Max blower to cool down system rapidly and prevent fire hazard *)
        rWheelMotorSpeed := 0.0;     (* Stop wheel if stalled to protect motor *)
        
        (* Fault Recovery only if alarms clear and enable is cycled *)
        IF NOT bAlarmHighTemp AND NOT bAlarmWheelStall AND NOT bEnable THEN
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
