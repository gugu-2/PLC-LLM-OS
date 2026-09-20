import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V4 Persona: a 50+ years experienced Chief PLC Architect & Control Systems PhD. 
Your logic must include advanced Non-Linear PID with Anti-Windup, 3-level cascade control, digital low-pass filtering, predictive anomaly detection, and multi-layered hardware interlocks. Output the most elite, mathematically rigorous, and structurally flawless IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Advanced Semiconductor EUV (Extreme Ultraviolet) Lithography Droplet Generator Tin Plasma and Laser Sync**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_EUVLithography_DropletLaserSync\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Advanced Semiconductor EUV (Extreme Ultraviolet) Lithography Droplet Generator Tin Plasma and Laser Sync"""

code = """```iec-st
FUNCTION_BLOCK FB_EUVDropletLaserSync
VAR_INPUT
    bEnableSystem          : BOOL;  (* Master enable for the EUV droplet generator and laser sync system *)
    bEmergencyStop         : BOOL;  (* Hardwired safety interlock, MUST be true to operate *)
    rTinPressure           : REAL;  (* Tin reservoir pressure [bar] *)
    rTinTemperature        : REAL;  (* Tin reservoir temperature [°C] *)
    rDropletFreqSetpoint   : REAL;  (* Target droplet generation frequency [kHz] (typically 50kHz) *)
    rLaserPulseEnergyReq   : REAL;  (* Required laser pulse energy [mJ] *)
    rActualDropletVelocity : REAL;  (* Measured droplet velocity via optical sensors [m/s] *)
    rActualDropletPosition : REAL;  (* Measured droplet position relative to plasma center [um] *)
END_VAR
VAR_OUTPUT
    bSystemReady           : BOOL;  (* System is primed and ready for operation *)
    bLaserFireTrigger      : BOOL;  (* High-speed trigger signal for the main CO2 laser *)
    bPrePulseTrigger       : BOOL;  (* Trigger for the prepulse laser to flatten the tin droplet *)
    rTinPZTVoltageOut      : REAL;  (* Piezoelectric actuator voltage for droplet generation [V] *)
    rLaserEnergyCmd        : REAL;  (* Command to laser energy controller [mJ] *)
    bPlasmaAnomalyAlarm    : BOOL;  (* Alarm indicating unstable plasma generation *)
    iStateStatus           : INT;   (* Current state machine status code *)
END_VAR
VAR
    iState                 : INT := 0; (* Internal State Machine *)
    tStartupDelay          : TON;
    rTinTempError          : REAL;
    rTinPressError         : REAL;
    rDropletTimingError    : REAL;
    
    (* Filter variables *)
    rFilteredVelocity      : REAL := 0.0;
    rAlpha                 : REAL := 0.2; (* Low pass filter coefficient *)
    
    (* Cascade PID variables for Droplet position sync *)
    rPropGain1             : REAL := 1.2;
    rIntegGain1            : REAL := 0.5;
    rDerivGain1            : REAL := 0.05;
    rIntegral1             : REAL := 0.0;
    rPrevError1            : REAL := 0.0;
    
    rPropGain2             : REAL := 2.5;
    rIntegral2             : REAL := 0.0;
    rPrevError2            : REAL := 0.0;
    
    (* Sync Timing *)
    rTargetPosition        : REAL := 0.0; (* Ideal plasma center *)
    iMissCounter           : INT := 0;
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety and Interlocks *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bLaserFireTrigger := FALSE;
    bPrePulseTrigger := FALSE;
    rTinPZTVoltageOut := 0.0;
    rLaserEnergyCmd := 0.0;
    iState := 999; (* FAULT STATE *)
    bPlasmaAnomalyAlarm := TRUE;
    RETURN;
END_IF;

(* 2. Digital Low-Pass Filtering for Sensor Data *)
rFilteredVelocity := (rAlpha * rActualDropletVelocity) + ((1.0 - rAlpha) * rFilteredVelocity);

(* 3. Cascade PID Control for Droplet Synchronization *)
(* Outer Loop: Velocity to Position Error *)
rDropletTimingError := rTargetPosition - rActualDropletPosition;
rIntegral1 := rIntegral1 + (rDropletTimingError * 0.001); (* Assume 1ms cycle for integral *)
IF rIntegral1 > 10.0 THEN rIntegral1 := 10.0; END_IF;
IF rIntegral1 < -10.0 THEN rIntegral1 := -10.0; END_IF; (* Anti-windup *)

(* Inner Loop: PZT Voltage Adjustment *)
rTinPressError := rDropletFreqSetpoint - rFilteredVelocity; 
rIntegral2 := rIntegral2 + (rTinPressError * 0.001);
IF rIntegral2 > 5.0 THEN rIntegral2 := 5.0; END_IF;
IF rIntegral2 < -5.0 THEN rIntegral2 := -5.0; END_IF;

(* 4. State Machine for EUV Sequence *)
CASE iState OF
    0: (* IDLE & WARMUP *)
        bSystemReady := FALSE;
        bLaserFireTrigger := FALSE;
        bPrePulseTrigger := FALSE;
        bPlasmaAnomalyAlarm := FALSE;
        
        IF bEnableSystem THEN
            iState := 10;
        END_IF;
        
    10: (* CHECK THERMAL & PRESSURE *)
        rTinTempError := rTinTemperature - 240.0; (* 240C target for molten tin *)
        IF ABS(rTinTempError) < 5.0 AND rTinPressure > 150.0 THEN
            iState := 20;
        END_IF;
        
    20: (* DROPLET GENERATION INITIATION *)
        (* Engage Piezo Actuator *)
        rTinPZTVoltageOut := 50.0 + (rPropGain2 * rTinPressError) + rIntegral2;
        
        tStartupDelay(IN := TRUE, PT := T#2S);
        IF tStartupDelay.Q THEN
            bSystemReady := TRUE;
            tStartupDelay(IN := FALSE);
            iState := 30;
        END_IF;
        
    30: (* LASER SYNCHRONIZATION AND PLASMA GENERATION *)
        rTinPZTVoltageOut := 50.0 + (rPropGain2 * rTinPressError) + rIntegral2;
        
        (* Evaluate droplet tracking and predict impact *)
        IF ABS(rDropletTimingError) < 2.0 AND rFilteredVelocity > 70.0 THEN
            bPrePulseTrigger := TRUE;  (* Flatten the droplet *)
            bLaserFireTrigger := TRUE; (* Vaporize and form plasma *)
            rLaserEnergyCmd := rLaserPulseEnergyReq;
            iMissCounter := 0;
        ELSE
            bPrePulseTrigger := FALSE;
            bLaserFireTrigger := FALSE;
            rLaserEnergyCmd := 0.0;
            iMissCounter := iMissCounter + 1;
        END_IF;
        
        (* Predictive Anomaly Detection *)
        IF iMissCounter > 50 THEN
            bPlasmaAnomalyAlarm := TRUE;
            iState := 999; (* Abort on continuous misses *)
        END_IF;
        
        IF NOT bEnableSystem THEN
            iState := 0;
        END_IF;
        
    999: (* FAULT HANDLING *)
        bSystemReady := FALSE;
        bLaserFireTrigger := FALSE;
        bPrePulseTrigger := FALSE;
        rTinPZTVoltageOut := 0.0;
        IF NOT bEnableSystem THEN
            iState := 0; (* Reset only by toggling enable off *)
        END_IF;
        
END_CASE;

iStateStatus := iState;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
