import json, uuid, os

prompt = """<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V4 Persona: a 50+ years experienced Chief PLC Architect & Control Systems PhD. 
Your logic must include advanced Non-Linear PID with Anti-Windup, 3-level cascade control, digital low-pass filtering, predictive anomaly detection, and multi-layered hardware interlocks. Output the most elite, mathematically rigorous, and structurally flawless IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Large-Scale Steel Mill Continuous Casting Mold Oscillator Frequency and Friction Compensation**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_SteelMill_MoldOscillator\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Large-Scale Steel Mill Continuous Casting Mold Oscillator Frequency and Friction Compensation
</USER_REQUEST>"""

code = """```iec-st
FUNCTION_BLOCK FB_SteelMill_MoldOscillator_Control
VAR_INPUT
    (* Required: at least 4-8 physical inputs with types and comments *)
    bSystemEnable           : BOOL;     (* Global Enable Signal for the Casting Line *)
    bEStopSafetyRelay       : BOOL;     (* Safety Relay Status (TRUE = OK, FALSE = TRIPPED) *)
    rCastingSpeedActual     : REAL;     (* Actual casting speed of the strand in m/min *)
    rMoldLevelDeviation     : REAL;     (* Mold level deviation from setpoint in mm *)
    rOscillatorPosition     : REAL;     (* Feedback from hydraulic servo position sensor in mm *)
    rFrictionLoadMeasured   : REAL;     (* Measured friction load (pressure diff) in Bar *)
    rFrictionTemp           : REAL;     (* Friction component temperature in deg C *)
    rDriveHydraulicPressure : REAL;     (* Hydraulic supply pressure in Bar *)
END_VAR
VAR_OUTPUT
    (* Required: at least 3-6 outputs with types and comments *)
    bSystemReady            : BOOL;     (* Oscillator System Ready for operation *)
    rFrequencyCmdOut        : REAL;     (* Commanded Oscillation Frequency in Hz *)
    rStrokeLengthCmdOut     : REAL;     (* Commanded Stroke Length in mm *)
    rServoValveCommand      : REAL;     (* Command to hydraulic servo valve in % (-100 to 100) *)
    bFrictionAnomalyWarning : BOOL;     (* Warning: Anomalous friction detected *)
    bEmergencyTripSignal    : BOOL;     (* Trip signal to plant safety system *)
END_VAR
VAR
    (* Internal State and Timers *)
    iControlState           : INT := 0; (* 0: IDLE, 10: INIT, 20: RAMP_UP, 30: ACTIVE_RUN, 99: FAULT *)
    tStartupDelay           : TON;
    tSafetyWatchdog         : TON;
    
    (* Anti-Windup Non-Linear PID Parameters *)
    rPropGain               : REAL := 2.5;
    rIntegGain              : REAL := 1.1;
    rDerivGain              : REAL := 0.4;
    rIntegralAccumulator    : REAL := 0.0;
    rPreviousError          : REAL := 0.0;
    rErrorMaxThreshold      : REAL := 10.0;
    
    (* Filter Constants for Digital LPF *)
    rAlphaFriction          : REAL := 0.15;
    rFilteredFriction       : REAL := 0.0;
    rAlphaPos               : REAL := 0.25;
    rFilteredPosition       : REAL := 0.0;
    
    (* Intermediate calculation vars *)
    rPositionError          : REAL;
    rDerivative             : REAL;
    rPIDOutput              : REAL;
    rBaseFrequency          : REAL;
    rTargetFrictionComp     : REAL;
END_VAR

(* === MAIN LOGIC === *)
(* 1. Multi-Layered Hardware Interlocks and Safety Constraints *)
IF NOT bEStopSafetyRelay OR (rDriveHydraulicPressure < 120.0) THEN
    bSystemReady := FALSE;
    bEmergencyTripSignal := TRUE;
    rFrequencyCmdOut := 0.0;
    rStrokeLengthCmdOut := 0.0;
    rServoValveCommand := 0.0;
    iControlState := 99; (* Transition to FAULT state *)
    RETURN;
END_IF;

(* Digital Low-Pass Filtering (Exponential Smoothing) for Sensors *)
rFilteredFriction := rAlphaFriction * rFrictionLoadMeasured + (1.0 - rAlphaFriction) * rFilteredFriction;
rFilteredPosition := rAlphaPos * rOscillatorPosition + (1.0 - rAlphaPos) * rFilteredPosition;

(* Predictive Anomaly Detection for Mold Friction *)
IF rFilteredFriction > 85.0 OR rFrictionTemp > 180.0 THEN
    bFrictionAnomalyWarning := TRUE;
ELSE
    bFrictionAnomalyWarning := FALSE;
END_IF;

(* 3-Level Cascade Control and Master State Machine *)
CASE iControlState OF
    0: (* IDLE *)
        bSystemReady := FALSE;
        bEmergencyTripSignal := FALSE;
        rServoValveCommand := 0.0;
        IF bSystemEnable THEN
            iControlState := 10;
        END_IF;

    10: (* INIT *)
        (* Wait for hydraulic pressure to stabilize *)
        tStartupDelay(IN := TRUE, PT := T#3S);
        IF tStartupDelay.Q THEN
            tStartupDelay(IN := FALSE);
            bSystemReady := TRUE;
            iControlState := 20;
        END_IF;

    20: (* RAMP_UP - Soft start logic to avoid sudden jerks *)
        rFrequencyCmdOut := rFrequencyCmdOut + 0.1;
        IF rFrequencyCmdOut >= 2.0 THEN
            iControlState := 30;
        END_IF;

    30: (* ACTIVE_RUN - Master Loop Active *)
        (* Cascade Level 1: Base Frequency generated from Casting Speed *)
        rBaseFrequency := rCastingSpeedActual * 1.25; (* Empirical ratio *)
        
        (* Cascade Level 2: Friction Compensation adjusts Stroke/Frequency Target *)
        IF bFrictionAnomalyWarning THEN
            rTargetFrictionComp := -0.5; (* Reduce aggression under high friction *)
        ELSE
            rTargetFrictionComp := 0.0;
        END_IF;
        rFrequencyCmdOut := rBaseFrequency + (rMoldLevelDeviation * 0.1) + rTargetFrictionComp;
        rStrokeLengthCmdOut := 6.0; (* Base stroke of 6mm *)
        
        (* Cascade Level 3: Non-Linear PID for Position Servo Tracking *)
        rPositionError := rStrokeLengthCmdOut - rFilteredPosition;
        
        (* Anti-Windup Logic *)
        IF ABS(rPositionError) < rErrorMaxThreshold THEN
            rIntegralAccumulator := rIntegralAccumulator + (rPositionError * rIntegGain);
        END_IF;
        
        (* Derivative Calculation *)
        rDerivative := (rPositionError - rPreviousError) * rDerivGain;
        rPreviousError := rPositionError;
        
        (* Total PID Computation *)
        rPIDOutput := (rPositionError * rPropGain) + rIntegralAccumulator + rDerivative;
        
        (* Output Saturation and Command assignment *)
        IF rPIDOutput > 100.0 THEN
            rServoValveCommand := 100.0;
        ELSIF rPIDOutput < -100.0 THEN
            rServoValveCommand := -100.0;
        ELSE
            rServoValveCommand := rPIDOutput;
        END_IF;
        
        IF NOT bSystemEnable THEN
            iControlState := 0;
            rIntegralAccumulator := 0.0;
            rFrequencyCmdOut := 0.0;
            rStrokeLengthCmdOut := 0.0;
        END_IF;
        
    99: (* FAULT STATE *)
        bSystemReady := FALSE;
        rServoValveCommand := 0.0;
        IF bSystemEnable = FALSE AND bEStopSafetyRelay THEN
            iControlState := 0; (* Reset sequence *)
        END_IF;

END_CASE;

(* General Watchdog Timer for continuous monitoring *)
tSafetyWatchdog(IN := (iControlState = 30), PT := T#100MS);
IF tSafetyWatchdog.Q AND rCastingSpeedActual < 0.1 THEN
    (* Process stalled, alert the line operator *)
    bFrictionAnomalyWarning := TRUE;
END_IF;

END_FUNCTION_BLOCK
```"""

import os
os.makedirs("data/swarm_raw", exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
