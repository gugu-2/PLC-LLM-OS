import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Commercial Scale Precision Fermentation Downstream Centrifuge**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Disk-stack continuous solids discharge profiling, feed rate proportional-integral decoupling from turbidity, and vibration harmonic imbalance trip). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

CRITICAL RULES - READ EVERY LINE:
1. CODE FENCE: Use TRIPLE backticks + iec-st. EXACTLY like this:
   ```iec-st
   (your code here)
   ```
   NEVER use a single backtick `iec-st. ALWAYS use triple backticks.
2. REQUIRED IEC 61131-3 STRUCTURE (all 5 mandatory):
   a. FUNCTION_BLOCK FB_<Name>   <- first line of code, always
   b. VAR_INPUT ... END_VAR      <- min 4 typed inputs with comments
   c. VAR_OUTPUT ... END_VAR     <- min 3 typed outputs with comments
   d. At least one END_IF; or END_CASE;  <- control logic required
   e. END_FUNCTION_BLOCK         <- last line of code, always
3. LENGTH: The assistant content MUST be >= 1500 characters total.
4. SAVE to isolated file using this exact Python:
"""

code = """```iec-st
FUNCTION_BLOCK FB_Fermentation_Centrifuge
VAR_INPUT
    (* Required: at least 4-8 physical inputs with types and comments *)
    bEnable                 : BOOL;     (* Main system enable command *)
    bEmergencyStop          : BOOL;     (* Safety relay health - TRUE = OK *)
    rInletTurbidity         : REAL;     (* Turbidity of feed (NTU) *)
    rFeedFlowRate           : REAL;     (* Current feed flow rate (L/hr) *)
    rBowlSpeedRPM           : REAL;     (* Centrifuge bowl speed (RPM) *)
    rVibrationSensorX       : REAL;     (* X-axis vibration (mm/s RMS) *)
    rVibrationSensorY       : REAL;     (* Y-axis vibration (mm/s RMS) *)
    rMotorTemperature       : REAL;     (* Motor winding temperature (deg C) *)
    tSolidsDischargeTime    : TIME;     (* Configured time interval for auto discharge *)
END_VAR
VAR_OUTPUT
    (* Required: at least 3-6 outputs with types and comments *)
    bSystemReady            : BOOL;     (* Centrifuge is ready for feed *)
    rTargetFeedPumpSpeed    : REAL;     (* Output speed to feed pump VFD (0-100%) *)
    bDischargeCommand       : BOOL;     (* Trigger for solids discharge cycle *)
    bAlarm                  : BOOL;     (* General fault alarm *)
    bCriticalTrip           : BOOL;     (* Imminent failure - immediate coast/brake required *)
    sStatusMessage          : STRING(50);(* Human readable state message *)
END_VAR
VAR
    (* Internal state variables *)
    iState                  : INT := 0; 
    tDischargeTimer         : TON;
    rFilteredVibrationX     : REAL;
    rFilteredVibrationY     : REAL;
    rIntegralError          : REAL := 0.0;
    rLastError              : REAL := 0.0;
    rDerivative             : REAL := 0.0;
    rPIDOutput              : REAL := 0.0;
    bFirstRun               : BOOL := TRUE;
    
    (* Filter Constants *)
    rAlpha                  : REAL := 0.15; (* Low pass filter coefficient *)
    
    (* PID Constants for Feed Rate Control based on Turbidity *)
    Kp                      : REAL := 2.5;
    Ki                      : REAL := 0.05;
    Kd                      : REAL := 0.1;
    rTargetTurbidity        : REAL := 15.0; (* Desired max turbidity in supernatant *)
    
    (* Limits *)
    rMaxVibration           : REAL := 8.5;  (* Max allowable vibration mm/s *)
    rTripVibration          : REAL := 14.0; (* Immediate trip vibration limit *)
    rMaxTemp                : REAL := 95.0; (* Motor max temp *)
END_VAR

(* === MAIN LOGIC === *)
(* Emergency Interlocks & Safety Layer *)
IF NOT bEmergencyStop THEN
    iState := 999; (* E-STOP STATE *)
    bSystemReady := FALSE;
    bAlarm := TRUE;
    bCriticalTrip := TRUE;
    sStatusMessage := 'E-STOP ACTIVE';
    rTargetFeedPumpSpeed := 0.0;
    bDischargeCommand := FALSE;
    RETURN;
END_IF;

(* Sensor Noise Filtering (EMA - Exponential Moving Average) *)
IF bFirstRun THEN
    rFilteredVibrationX := rVibrationSensorX;
    rFilteredVibrationY := rVibrationSensorY;
    bFirstRun := FALSE;
ELSE
    rFilteredVibrationX := rFilteredVibrationX + rAlpha * (rVibrationSensorX - rFilteredVibrationX);
    rFilteredVibrationY := rFilteredVibrationY + rAlpha * (rVibrationSensorY - rFilteredVibrationY);
END_IF;

(* Critical Hardware Protection Overrides *)
IF (rFilteredVibrationX > rTripVibration) OR (rFilteredVibrationY > rTripVibration) OR (rMotorTemperature > rMaxTemp) THEN
    iState := 999;
    bCriticalTrip := TRUE;
    bAlarm := TRUE;
    rTargetFeedPumpSpeed := 0.0;
    sStatusMessage := 'TRIP: VIBRATION/TEMP LIMIT';
    RETURN;
END_IF;

(* Standard Operation State Machine *)
CASE iState OF
    0: (* IDLE *)
        bSystemReady := FALSE;
        rTargetFeedPumpSpeed := 0.0;
        bDischargeCommand := FALSE;
        sStatusMessage := 'IDLE';
        IF bEnable THEN
            iState := 10;
        END_IF;

    10: (* RAMP UP & STABILIZE *)
        sStatusMessage := 'RAMP UP & STABILIZATION';
        (* Wait for bowl speed to reach operational target e.g. 7000 RPM *)
        IF rBowlSpeedRPM > 6800.0 THEN
            bSystemReady := TRUE;
            iState := 20;
            (* Reset PID parameters before switching to run mode *)
            rIntegralError := 0.0;
            rLastError := rTargetTurbidity - rInletTurbidity;
        END_IF;
        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    20: (* RUNNING: DYNAMIC FEED CONTROL & DISCHARGE CYCLING *)
        sStatusMessage := 'RUNNING: DYNAMIC CONTROL';
        
        (* Feed Rate PID Control based on Inlet Turbidity *)
        (* High turbidity requires slower feed to allow adequate separation time *)
        rLastError := rTargetTurbidity - rInletTurbidity;
        rIntegralError := rIntegralError + (rLastError * 0.1); (* Assuming 100ms cycle time *)
        
        (* Anti-windup protection *)
        IF rIntegralError > 100.0 THEN rIntegralError := 100.0; END_IF;
        IF rIntegralError < -100.0 THEN rIntegralError := -100.0; END_IF;
        
        rDerivative := (rLastError - rPIDOutput) / 0.1;
        rPIDOutput := (Kp * rLastError) + (Ki * rIntegralError) + (Kd * rDerivative);
        
        (* Map PID output to pump speed (0-100%). Baseline speed is 50% *)
        rTargetFeedPumpSpeed := 50.0 + rPIDOutput;
        
        IF rTargetFeedPumpSpeed > 100.0 THEN rTargetFeedPumpSpeed := 100.0; END_IF;
        IF rTargetFeedPumpSpeed < 10.0 THEN rTargetFeedPumpSpeed := 10.0; END_IF;

        (* Warning levels for vibration *)
        IF (rFilteredVibrationX > rMaxVibration) OR (rFilteredVibrationY > rMaxVibration) THEN
            bAlarm := TRUE;
            (* Throttle feed back to reduce load *)
            rTargetFeedPumpSpeed := rTargetFeedPumpSpeed * 0.5;
        ELSE
            bAlarm := FALSE;
        END_IF;

        (* Solids Discharge Timer Management *)
        tDischargeTimer(IN := TRUE, PT := tSolidsDischargeTime);
        IF tDischargeTimer.Q THEN
            tDischargeTimer(IN := FALSE);
            iState := 30;
        END_IF;

        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    30: (* DISCHARGE SEQUENCE *)
        sStatusMessage := 'DISCHARGE ACTIVE';
        bDischargeCommand := TRUE;
        (* In a real scenario, wait for discharge completion feedback. Here we simulate 1 scan trigger *)
        bDischargeCommand := FALSE; 
        iState := 20;

    999: (* FAULT TRIPPED *)
        bSystemReady := FALSE;
        rTargetFeedPumpSpeed := 0.0;
        bDischargeCommand := FALSE;
        IF NOT bCriticalTrip AND bEnable THEN
            (* Fault reset attempt *)
            bAlarm := FALSE;
            iState := 0;
        END_IF;
        
END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
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
