import json, uuid, os
os.makedirs("data/swarm_raw", exist_ok=True)
prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: High-Altitude Atmospheric Research Balloon Helium Vent Valve and Ballast Drop Sync**

Task: Invent a highly complex, ultra-realistic control scenario for this domain. Make this code EVEN BETTER, MORE ADVANCED, and MORE RIGOROUS than previous iterations. Include extreme edge-case handling, advanced math, and robust fault-tolerance.

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
   import json, uuid
   prompt = \"\"\"<copy this exact user prompt here>\"\"\"
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_AeroBalloon_FlightControl\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
   record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
   with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
       json.dump(record, f, ensure_ascii=False)
5. SELF-CHECK before saving - verify ALL:
   [ ] Fence is ```iec-st
   [ ] First code line: FUNCTION_BLOCK FB_<name>
   [ ] Has VAR_INPUT section
   [ ] Has VAR_OUTPUT section
   [ ] Has END_IF; or END_CASE;
   [ ] Last code line: END_FUNCTION_BLOCK
   [ ] Closing fence: ```
   [ ] Total chars >= 1500
6. REPLY with: EVOLUTION COMPLETE: High-Altitude Atmospheric Research Balloon Helium Vent Valve and Ballast Drop Sync

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_AeroBalloon_FlightControl
VAR_INPUT
    bSystemEnable           : BOOL;     (* System master enable for automated flight control *)
    bEmergencyAbort         : BOOL;     (* Immediate abort: open all vents, drop all ballast *)
    rAltitudeMeters         : REAL;     (* Current MSL altitude from redundant GPS/barometric sensors *)
    rTargetAltitudeMeters   : REAL;     (* Target MSL altitude for mission profile phase *)
    rAscentRateMps          : REAL;     (* Current ascent rate in meters per second *)
    rInternalGasTempC       : REAL;     (* Helium envelope internal temperature in Celsius *)
    rExternalAirTempC       : REAL;     (* External ambient air temperature in Celsius *)
    rAvailableBallastKg     : REAL;     (* Remaining mass of ballast on board in kg *)
    bVentValvePositionLimit : BOOL;     (* Hardware limit switch indicating vent is fully open *)
END_VAR
VAR_OUTPUT
    bVentValveCommand       : BOOL;     (* Command to open the helium vent valve (TRUE = open) *)
    rVentValveAnalogPos     : REAL;     (* Analog command (0.0 to 100.0%) for proportional vent valve *)
    bBallastDropCommand     : BOOL;     (* Command to actuate the ballast drop mechanism *)
    rBallastDropRateKgPs    : REAL;     (* Calculated ballast drop rate required in kg/sec *)
    bMissionComplete        : BOOL;     (* High-level indicator that flight profile is complete *)
    bCriticalAlarm          : BOOL;     (* Indicates a catastrophic failure or unsafe state *)
    iFlightPhase            : INT;      (* Current mission phase (0=Ground, 1=Ascent, 2=Float, 3=Descent) *)
END_VAR
VAR
    iState                  : INT := 0; (* Internal state machine *)
    tVentValveTimer         : TON;      (* Timer to prevent valve chatter *)
    tBallastTimer           : TON;      (* Timer for pulsed ballast release *)
    rAltitudeError          : REAL;     (* Difference between target and actual altitude *)
    rDensityRatio           : REAL;     (* Simplified atmospheric density ratio for lift calc *)
    rLiftDeficit            : REAL;     (* Calculated lift deficit requiring ballast drop *)
    rVolumeChange           : REAL;     (* Gas volume expansion effect derived from temps *)
    rIntegralAscentError    : REAL := 0.0;
    rPreviousAscentError    : REAL := 0.0;
    rAscentError            : REAL;
    rKp                     : REAL := 2.5;
    rKi                     : REAL := 0.05;
    rKd                     : REAL := 0.1;
    rDerivativeAscentError  : REAL;
    rPIDOutput              : REAL;
    bInitializePID          : BOOL := TRUE;
END_VAR

(* === MAIN LOGIC === *)
IF bEmergencyAbort THEN
    bVentValveCommand := TRUE; 
    rVentValveAnalogPos := 100.0;
    bBallastDropCommand := TRUE; 
    rBallastDropRateKgPs := 5.0; 
    bCriticalAlarm := TRUE;
    iState := 999;
    RETURN;
END_IF;

IF NOT bSystemEnable THEN
    bVentValveCommand := FALSE;
    rVentValveAnalogPos := 0.0;
    bBallastDropCommand := FALSE;
    rBallastDropRateKgPs := 0.0;
    bCriticalAlarm := FALSE;
    iState := 0;
    RETURN;
END_IF;

rAltitudeError := rTargetAltitudeMeters - rAltitudeMeters;
rVolumeChange := (rInternalGasTempC + 273.15) / (rExternalAirTempC + 273.15);

CASE iState OF
    0: (* INIT AND GROUND CHECK *)
        bMissionComplete := FALSE;
        iFlightPhase := 0;
        bInitializePID := TRUE;
        IF bSystemEnable AND (rAltitudeMeters < 500.0) THEN
            iState := 10;
        END_IF;

    10: (* ASCENT PHASE *)
        iFlightPhase := 1;
        
        (* Target an ascent rate of 3.5 m/s *)
        rAscentError := 3.5 - rAscentRateMps;
        
        IF bInitializePID THEN
            rIntegralAscentError := 0.0;
            rPreviousAscentError := rAscentError;
            bInitializePID := FALSE;
        END_IF;
        
        rIntegralAscentError := rIntegralAscentError + rAscentError;
        rDerivativeAscentError := rAscentError - rPreviousAscentError;
        
        rPIDOutput := (rKp * rAscentError) + (rKi * rIntegralAscentError) + (rKd * rDerivativeAscentError);
        rPreviousAscentError := rAscentError;
        
        IF rPIDOutput > 10.0 THEN
            bBallastDropCommand := TRUE;
            rBallastDropRateKgPs := 0.2; (* Gentle drop *)
        ELSE
            bBallastDropCommand := FALSE;
            rBallastDropRateKgPs := 0.0;
        END_IF;
        
        IF rPIDOutput < -5.0 THEN
            bVentValveCommand := TRUE;
            rVentValveAnalogPos := 15.0;
        ELSE
            bVentValveCommand := FALSE;
            rVentValveAnalogPos := 0.0;
        END_IF;
        
        IF rAltitudeError <= 50.0 THEN
            iState := 20;
            bInitializePID := TRUE;
        END_IF;

    20: (* FLOAT PHASE *)
        iFlightPhase := 2;
        
        (* Maintain target altitude *)
        IF ABS(rAltitudeError) > 200.0 THEN
            IF rAltitudeError > 0.0 THEN
                (* We are too low, drop ballast if available *)
                IF rAvailableBallastKg > 5.0 THEN
                    tBallastTimer(IN := NOT tBallastTimer.Q, PT := T#2S);
                    bBallastDropCommand := tBallastTimer.Q;
                    rBallastDropRateKgPs := 0.5;
                END_IF;
                bVentValveCommand := FALSE;
                rVentValveAnalogPos := 0.0;
            ELSE
                (* We are too high, vent helium *)
                tVentValveTimer(IN := NOT tVentValveTimer.Q, PT := T#3S);
                bVentValveCommand := tVentValveTimer.Q;
                rVentValveAnalogPos := 25.0;
                bBallastDropCommand := FALSE;
                rBallastDropRateKgPs := 0.0;
            END_IF;
        ELSE
            bVentValveCommand := FALSE;
            rVentValveAnalogPos := 0.0;
            bBallastDropCommand := FALSE;
            rBallastDropRateKgPs := 0.0;
        END_IF;
        
        IF rTargetAltitudeMeters < 1000.0 THEN
            iState := 30;
        END_IF;

    30: (* DESCENT PHASE *)
        iFlightPhase := 3;
        
        (* Target a descent rate of -2.5 m/s *)
        rAscentError := -2.5 - rAscentRateMps;
        
        IF rAscentError > 1.0 THEN
            (* Descending too fast, drop ballast *)
            bBallastDropCommand := TRUE;
            rBallastDropRateKgPs := 0.8;
            bVentValveCommand := FALSE;
        ELSIF rAscentError < -1.0 THEN
            (* Descending too slow, vent more *)
            bVentValveCommand := TRUE;
            rVentValveAnalogPos := 40.0;
            bBallastDropCommand := FALSE;
        ELSE
            bBallastDropCommand := FALSE;
            bVentValveCommand := FALSE;
            rVentValveAnalogPos := 0.0;
        END_IF;
        
        IF rAltitudeMeters < 100.0 THEN
            iState := 40;
        END_IF;
        
    40: (* MISSION COMPLETE / LANDING *)
        bMissionComplete := TRUE;
        bVentValveCommand := TRUE; (* Dump remaining helium *)
        rVentValveAnalogPos := 100.0;
        bBallastDropCommand := FALSE;
        rBallastDropRateKgPs := 0.0;
        
    999: (* FAULT / ABORT STATE *)
        bCriticalAlarm := TRUE;
        bVentValveCommand := TRUE;
        rVentValveAnalogPos := 100.0;
        bBallastDropCommand := TRUE;
        
END_CASE;

END_FUNCTION_BLOCK
```"""
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
