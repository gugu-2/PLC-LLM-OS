import json
import uuid
import os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V4 Persona: a 50+ years experienced Chief PLC Architect & Control Systems PhD. 
Your logic must include advanced Non-Linear PID with Anti-Windup, 3-level cascade control, digital low-pass filtering, predictive anomaly detection, and multi-layered hardware interlocks. Output the most elite, mathematically rigorous, and structurally flawless IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Automated Astronomical Observatory Enclosure Dome Slit Synchronization and Telescope Azimuth Matching**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Observatory_DomeSync\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Automated Astronomical Observatory Enclosure Dome Slit Synchronization and Telescope Azimuth Matching"""

code = """```iec-st
FUNCTION_BLOCK FB_Observatory_DomeSync
VAR_INPUT
    (* System Master Controls *)
    bEnable               : BOOL;     (* System master enable signal *)
    bEmergencyStop        : BOOL;     (* Hardware E-Stop OK (Normally Closed loop) *)
    
    (* Telescope Telemetry *)
    rTelescopeAzimuth     : REAL;     (* Current telescope azimuth [0.0 - 360.0 deg] *)
    rTelescopeVelocity    : REAL;     (* Current telescope slew velocity [deg/s] *)
    
    (* Dome Telemetry *)
    rDomeAzimuth          : REAL;     (* Current dome slit azimuth [0.0 - 360.0 deg] *)
    rDomeVelocityMeasured : REAL;     (* Feedback from dome drive encoder [deg/s] *)
    rDomeMotorCurrent     : REAL;     (* Inverter output current to dome drive motor [A] *)
    
    (* Environmental Sensors *)
    bWindLimitExceeded    : BOOL;     (* Anemometer limit switch triggered *)
    rWindSpeed            : REAL;     (* Current wind speed [m/s] *)
    rTemperatureAmbient   : REAL;     (* Ambient temperature for mechanical friction compensation [C] *)
END_VAR
VAR_OUTPUT
    (* System Status Flags *)
    bSystemReady          : BOOL;     (* Dome tracking system is initialized and ready *)
    bDomeTrackingOk       : BOOL;     (* Dome is within acceptable azimuth error tolerance *)
    bSafetyInterlockActive: BOOL;     (* Hardware or software safety interlock engaged *)
    bAlarm                : BOOL;     (* General fault alarm output *)
    iErrorCode            : INT;      (* Detailed diagnostic error code for SCADA integration *)
    
    (* Physical Actuator Commands *)
    rDomePWM_Signal       : REAL;     (* Final command to Dome Drive VFD [-100.0 to 100.0 %] *)
END_VAR
VAR
    (* Main State Machine *)
    iState                : INT := 0; (* Main State Machine Step *)
    tTimer                : TON;      (* State transition timer *)
    tWatchdog             : TON;      (* System liveness watchdog *)
    
    (* Filtering Variables (Butterworth approximation) *)
    rTelAzimuthFiltered   : REAL;
    rDomeAzimuthFiltered  : REAL;
    rDomeVelFiltered      : REAL;
    rAlphaFilter          : REAL := 0.15; (* Low-pass filter coefficient for positional data *)
    rVelAlphaFilter       : REAL := 0.25; (* Filter for high-frequency velocity noise *)
    
    (* Position Loop (Outer) Variables *)
    rAzimuthError         : REAL;     (* Shortest path azimuth error [-180.0 to 180.0] *)
    rPosErrorIntegral     : REAL;
    rPosErrorDerivative   : REAL;
    rLastPosError         : REAL;
    rPosKp                : REAL := 2.75;
    rPosKi                : REAL := 0.12;
    rPosKd                : REAL := 0.45;
    rPosIntegralLimit     : REAL := 20.0;
    rDesiredVelocity      : REAL;     (* Output of Position Loop *)
    
    (* Velocity Loop (Middle) Variables *)
    rVelError             : REAL;
    rVelErrorIntegral     : REAL;
    rVelKp                : REAL := 5.50;
    rVelKi                : REAL := 1.20;
    rVelIntegralLimit     : REAL := 50.0;
    rDesiredCurrent       : REAL;     (* Output of Velocity Loop *)
    
    (* Current Loop (Inner) Variables *)
    rCurrError            : REAL;
    rCurrErrorIntegral    : REAL;
    rCurrKp               : REAL := 10.0;
    rCurrKi               : REAL := 5.0;
    rCurrIntegralLimit    : REAL := 100.0;
    rFinalPWM             : REAL;     (* Output of Current Loop *)
    
    (* Kinematic Feed-Forward *)
    rFeedForwardGain      : REAL := 0.85;
    rPredictedFriction    : REAL;
    
    (* Output clamping *)
    rMaxPWM               : REAL := 100.0;
    
    (* Status & Fault flags *)
    bInternalFault        : BOOL := FALSE;
END_VAR

(* === MAIN LOGIC === *)
(* 1. Multi-Layered Hardware & Safety Interlocks *)
IF NOT bEmergencyStop OR bWindLimitExceeded THEN
    bSystemReady := FALSE;
    bSafetyInterlockActive := TRUE;
    bAlarm := TRUE;
    rDomePWM_Signal := 0.0;
    
    IF NOT bEmergencyStop THEN
        iErrorCode := 9001; (* CRITICAL: E-STOP Activated *)
    ELSIF bWindLimitExceeded THEN
        iErrorCode := 9002; (* CRITICAL: Wind Limit Exceeded (> 20 m/s) *)
    END_IF;
    
    iState := 0; (* Force to idle *)
    RETURN;
ELSE
    bSafetyInterlockActive := FALSE;
    bAlarm := bInternalFault;
END_IF;

(* 2. Digital Low-Pass Filtering for Noisy Encoders *)
rTelAzimuthFiltered  := (rAlphaFilter * rTelescopeAzimuth) + ((1.0 - rAlphaFilter) * rTelAzimuthFiltered);
rDomeAzimuthFiltered := (rAlphaFilter * rDomeAzimuth) + ((1.0 - rAlphaFilter) * rDomeAzimuthFiltered);
rDomeVelFiltered     := (rVelAlphaFilter * rDomeVelocityMeasured) + ((1.0 - rVelAlphaFilter) * rDomeVelFiltered);

(* 3. Shortest Path Azimuth Error Calculation (Accounting for 360 wrap-around) *)
rAzimuthError := rTelAzimuthFiltered - rDomeAzimuthFiltered;
IF rAzimuthError > 180.0 THEN
    rAzimuthError := rAzimuthError - 360.0;
ELSIF rAzimuthError < -180.0 THEN
    rAzimuthError := rAzimuthError + 360.0;
END_IF;

(* 4. State Machine Implementation for 3-Level Cascade Control *)
CASE iState OF
    0: (* IDLE & INITIALIZATION *)
        rDomePWM_Signal := 0.0;
        bSystemReady := FALSE;
        bDomeTrackingOk := FALSE;
        
        (* Reset all integrators *)
        rPosErrorIntegral := 0.0;
        rVelErrorIntegral := 0.0;
        rCurrErrorIntegral := 0.0;
        
        IF bEnable AND NOT bAlarm THEN
            iState := 10;
        END_IF;

    10: (* WARM-UP & PRE-CHECK *)
        tTimer(IN := TRUE, PT := T#2S);
        IF tTimer.Q THEN
            tTimer(IN := FALSE);
            bSystemReady := TRUE;
            iState := 20;
        END_IF;

    20: (* ACTIVE TRACKING - 3-LEVEL CASCADE NON-LINEAR PID *)
        IF NOT bEnable THEN
            iState := 0;
        END_IF;
        
        (* ------------------------------------------------------------- *)
        (* LEVEL 1: POSITION LOOP (Calculates Desired Velocity)          *)
        (* ------------------------------------------------------------- *)
        
        (* Non-Linear Proportional Gain for Position (aggressive for large errors) *)
        IF ABS(rAzimuthError) > 15.0 THEN
            rPosKp := 4.5; 
        ELSE
            rPosKp := 2.75;
        END_IF;
        
        (* Position Integral Term with Anti-Windup *)
        IF ABS(rAzimuthError) < 5.0 THEN
            rPosErrorIntegral := rPosErrorIntegral + (rAzimuthError * 0.1); (* 100ms cycle *)
            IF rPosErrorIntegral > rPosIntegralLimit THEN
                rPosErrorIntegral := rPosIntegralLimit;
            ELSIF rPosErrorIntegral < -rPosIntegralLimit THEN
                rPosErrorIntegral := -rPosIntegralLimit;
            END_IF;
        ELSE
            rPosErrorIntegral := 0.0; (* Prevent massive overshoot during fast slews *)
        END_IF;
        
        rPosErrorDerivative := (rAzimuthError - rLastPosError) / 0.1;
        rLastPosError := rAzimuthError;
        
        rDesiredVelocity := (rPosKp * rAzimuthError) + (rPosKi * rPosErrorIntegral) + (rPosKd * rPosErrorDerivative) + (rTelescopeVelocity * rFeedForwardGain);
        
        (* ------------------------------------------------------------- *)
        (* LEVEL 2: VELOCITY LOOP (Calculates Desired Current)           *)
        (* ------------------------------------------------------------- *)
        
        rVelError := rDesiredVelocity - rDomeVelFiltered;
        rVelErrorIntegral := rVelErrorIntegral + (rVelError * 0.1);
        
        IF rVelErrorIntegral > rVelIntegralLimit THEN rVelErrorIntegral := rVelIntegralLimit; END_IF;
        IF rVelErrorIntegral < -rVelIntegralLimit THEN rVelErrorIntegral := -rVelIntegralLimit; END_IF;
        
        (* Environmental stiction/friction compensation based on temperature *)
        IF rTemperatureAmbient < 0.0 THEN
            rPredictedFriction := 5.0; (* Additional torque required in cold weather *)
        ELSE
            rPredictedFriction := 1.0;
        END_IF;
        
        rDesiredCurrent := (rVelKp * rVelError) + (rVelKi * rVelErrorIntegral);
        
        (* Apply directional friction compensation *)
        IF rDesiredVelocity > 0.1 THEN
            rDesiredCurrent := rDesiredCurrent + rPredictedFriction;
        ELSIF rDesiredVelocity < -0.1 THEN
            rDesiredCurrent := rDesiredCurrent - rPredictedFriction;
        END_IF;
        
        (* ------------------------------------------------------------- *)
        (* LEVEL 3: CURRENT LOOP (Calculates Final PWM Signal)           *)
        (* ------------------------------------------------------------- *)
        
        rCurrError := rDesiredCurrent - rDomeMotorCurrent;
        rCurrErrorIntegral := rCurrErrorIntegral + (rCurrError * 0.1);
        
        IF rCurrErrorIntegral > rCurrIntegralLimit THEN rCurrErrorIntegral := rCurrIntegralLimit; END_IF;
        IF rCurrErrorIntegral < -rCurrIntegralLimit THEN rCurrErrorIntegral := -rCurrIntegralLimit; END_IF;
        
        rFinalPWM := (rCurrKp * rCurrError) + (rCurrKi * rCurrErrorIntegral);
        
        (* Output Signal Saturation Clamp *)
        IF rFinalPWM > rMaxPWM THEN
            rFinalPWM := rMaxPWM;
        ELSIF rFinalPWM < -rMaxPWM THEN
            rFinalPWM := -rMaxPWM;
        END_IF;
        
        (* Final Output Assignment & Deadband Processing *)
        IF ABS(rAzimuthError) < 0.25 THEN
            rDomePWM_Signal := 0.0; (* Prevent micro-jitter when perfectly aligned *)
            bDomeTrackingOk := TRUE;
        ELSE
            rDomePWM_Signal := rFinalPWM;
            bDomeTrackingOk := FALSE;
        END_IF;
        
        (* ------------------------------------------------------------- *)
        (* PREDICTIVE ANOMALY DETECTION                                  *)
        (* ------------------------------------------------------------- *)
        (* High PWM command but no motor movement implies stall or failure *)
        IF ABS(rDomePWM_Signal) > 80.0 AND ABS(rDomeVelFiltered) < 0.1 THEN
            tWatchdog(IN := TRUE, PT := T#3S);
            IF tWatchdog.Q THEN
                bInternalFault := TRUE;
                iErrorCode := 8005; (* ERR: Drive Stall or Mechanical Jam *)
                iState := 99; (* Transition to Fault State *)
            END_IF;
        ELSE
            tWatchdog(IN := FALSE);
        END_IF;

    99: (* FAULT HANDLING *)
        rDomePWM_Signal := 0.0;
        bSystemReady := FALSE;
        bDomeTrackingOk := FALSE;
        bAlarm := TRUE;
        
        IF NOT bEnable THEN
            bInternalFault := FALSE;
            tWatchdog(IN := FALSE);
            iState := 0; (* Require manual disable/re-enable to clear fault *)
        END_IF;
        
END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
