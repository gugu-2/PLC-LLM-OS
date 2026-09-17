import os, json, uuid

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Commercial Greenhouse Automated Climate Control Shading and CO2 Enrichment**

Task: Invent a highly complex, ultra-realistic control scenario for this domain. Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Greenhouse_ClimateControl\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Commercial Greenhouse Automated Climate Control Shading and CO2 Enrichment

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.
</USER_REQUEST>"""

code = """```iec-st
FUNCTION_BLOCK FB_Greenhouse_Climate_Shading_CO2
VAR_INPUT
    (* Operational Inputs *)
    bSystemEnable       : BOOL;     (* Master enable for the greenhouse climate control system *)
    bEmergencyStop      : BOOL;     (* Hardware E-Stop OK relay signal (FALSE = Stop) *)
    bFireAlarm          : BOOL;     (* Fire alarm interlock (TRUE = Fire Detected) *)
    
    (* Environmental Sensors - Assumed scaled 4-20mA or digital readings *)
    rIndoorTemp         : REAL;     (* Current indoor temperature in degrees Celsius *)
    rOutdoorTemp        : REAL;     (* Current outdoor temperature in degrees Celsius *)
    rIndoorHumidity     : REAL;     (* Current indoor relative humidity (%) *)
    rSolarRadiation     : REAL;     (* Current solar radiation in W/m^2 *)
    rWindSpeed          : REAL;     (* Current outdoor wind speed in m/s *)
    rCO2PPM             : REAL;     (* Current indoor CO2 concentration in Parts Per Million (PPM) *)
    
    (* Setpoints & Config *)
    rTempSetpointDay    : REAL;     (* Target daytime temperature (Deg C) *)
    rTempSetpointNight  : REAL;     (* Target nighttime temperature (Deg C) *)
    rCO2Setpoint        : REAL;     (* Target CO2 concentration (PPM) *)
    rMaxRadiation       : REAL;     (* Maximum allowed solar radiation before shading (W/m^2) *)
    bDayTimeMode        : BOOL;     (* TRUE if currently daytime mode, FALSE if nighttime *)
END_VAR

VAR_OUTPUT
    (* Actuator Commands *)
    rShadingPosition    : REAL;     (* Shade screen position command 0.0 to 100.0% (100 = fully closed) *)
    bCO2ValveOpen       : BOOL;     (* Solenoid valve command for CO2 enrichment tank *)
    rVentilationPos     : REAL;     (* Roof vent position command 0.0 to 100.0% *)
    
    (* System Status & Alarms *)
    bSystemActive       : BOOL;     (* TRUE when control loops are actively running *)
    bShadingInterlock   : BOOL;     (* TRUE when shading is disabled due to high wind / emergency *)
    bAlarmHighTemp      : BOOL;     (* Alarm: Temperature exceeds critical threshold *)
    bAlarmCO2Fault      : BOOL;     (* Alarm: CO2 sensor error or regulation failed *)
    bSystemFault        : BOOL;     (* General system fault indicator *)
END_VAR

VAR
    (* Internal State and Timers *)
    iControlState       : INT := 0; (* 0=Init, 10=Idle, 20=Active, 99=Fault *)
    tControlLoopTimer   : TON;
    tCO2DelayTimer      : TON;
    
    (* Filtered Variables (Exponential Moving Average) *)
    rFiltSolarRad       : REAL := 0.0;
    rFiltWindSpeed      : REAL := 0.0;
    rFiltCO2PPM         : REAL := 400.0;
    
    (* Filter Constants *)
    rAlphaRad           : REAL := 0.1;
    rAlphaWind          : REAL := 0.2;
    rAlphaCO2           : REAL := 0.05;
    
    (* Working Variables *)
    rActiveTempSP       : REAL;
    rTempError          : REAL;
    rCO2Error           : REAL;
    
    (* Limits *)
    c_rMaxWindSpeed     : REAL := 15.0; (* m/s - wind threshold to retract shades *)
    c_rHighTempLimit    : REAL := 40.0; (* Deg C - absolute maximum safe temperature *)
END_VAR

(* ==============================================================================
   MAIN LOGIC
   ============================================================================== *)

(* 1. Safety and Interlock Processing *)
IF NOT bEmergencyStop OR bFireAlarm THEN
    iControlState := 99; (* Transition to fault state *)
    bSystemFault := TRUE;
    
    (* Override Actuators for Safety *)
    rShadingPosition := 0.0; (* Retract shades to avoid trapping heat/smoke *)
    bCO2ValveOpen := FALSE;  (* Secure CO2 supply *)
    rVentilationPos := 100.0; (* Open vents fully for smoke evacuation if fire *)
    
    bSystemActive := FALSE;
    RETURN;
END_IF;

(* 2. Signal Filtering (First Order EMA for noise reduction) *)
rFiltSolarRad := (rAlphaRad * rSolarRadiation) + ((1.0 - rAlphaRad) * rFiltSolarRad);
rFiltWindSpeed := (rAlphaWind * rWindSpeed) + ((1.0 - rAlphaWind) * rFiltWindSpeed);
rFiltCO2PPM := (rAlphaCO2 * rCO2PPM) + ((1.0 - rAlphaCO2) * rFiltCO2PPM);

(* 3. Setpoint Determination *)
IF bDayTimeMode THEN
    rActiveTempSP := rTempSetpointDay;
ELSE
    rActiveTempSP := rTempSetpointNight;
END_IF;

(* 4. Alarm Generation *)
IF rIndoorTemp > c_rHighTempLimit THEN
    bAlarmHighTemp := TRUE;
ELSE
    bAlarmHighTemp := FALSE;
END_IF;

IF (rFiltCO2PPM < 100.0) OR (rFiltCO2PPM > 5000.0) THEN
    bAlarmCO2Fault := TRUE; (* Sensor likely out of bounds / failed *)
ELSE
    bAlarmCO2Fault := FALSE;
END_IF;

(* 5. State Machine Control *)
CASE iControlState OF
    0: (* INIT *)
        bSystemActive := FALSE;
        rShadingPosition := 0.0;
        bCO2ValveOpen := FALSE;
        rVentilationPos := 0.0;
        bSystemFault := FALSE;
        
        IF bSystemEnable THEN
            iControlState := 10;
        END_IF;

    10: (* IDLE *)
        bSystemActive := FALSE;
        IF bSystemEnable AND NOT bSystemFault THEN
            iControlState := 20;
        ELSIF NOT bSystemEnable THEN
            rShadingPosition := 0.0;
            bCO2ValveOpen := FALSE;
            rVentilationPos := 0.0;
        END_IF;

    20: (* ACTIVE CONTROL LOOP *)
        bSystemActive := TRUE;
        
        (* If system is disabled, go back to idle *)
        IF NOT bSystemEnable THEN
            iControlState := 10;
        END_IF;
        
        (* === Shading Control === *)
        (* High wind interlock: retract shades to prevent mechanical damage *)
        IF rFiltWindSpeed > c_rMaxWindSpeed THEN
            bShadingInterlock := TRUE;
            rShadingPosition := 0.0; 
        ELSE
            bShadingInterlock := FALSE;
            (* Modulate shading based on solar radiation *)
            IF rFiltSolarRad > rMaxRadiation THEN
                (* Proportional shading based on excess radiation *)
                rShadingPosition := LIMIT(0.0, ((rFiltSolarRad - rMaxRadiation) / 200.0) * 100.0, 100.0);
            ELSE
                rShadingPosition := 0.0;
            END_IF;
        END_IF;
        
        (* === Ventilation Control (Simple Proportional) === *)
        rTempError := rIndoorTemp - rActiveTempSP;
        IF rTempError > 1.0 THEN
            (* Open vents progressively if temperature is too high *)
            rVentilationPos := LIMIT(0.0, (rTempError / 5.0) * 100.0, 100.0);
        ELSE
            rVentilationPos := 0.0;
        END_IF;
        
        (* === CO2 Enrichment Control === *)
        (* Only enrich CO2 during daytime when photosynthesis is active, 
           vents are not fully open (to avoid wasting gas), and no faults exist *)
        IF bDayTimeMode AND (rVentilationPos < 50.0) AND NOT bAlarmCO2Fault THEN
            rCO2Error := rCO2Setpoint - rFiltCO2PPM;
            
            (* Hysteresis control for CO2 valve *)
            IF rCO2Error > 50.0 THEN
                tCO2DelayTimer(IN := TRUE, PT := T#5S); (* Debounce *)
                IF tCO2DelayTimer.Q THEN
                    bCO2ValveOpen := TRUE;
                END_IF;
            ELSIF rCO2Error < 0.0 THEN
                bCO2ValveOpen := FALSE;
                tCO2DelayTimer(IN := FALSE, PT := T#5S);
            END_IF;
        ELSE
            bCO2ValveOpen := FALSE;
            tCO2DelayTimer(IN := FALSE, PT := T#5S);
        END_IF;
        
    99: (* FAULT STATE *)
        bSystemActive := FALSE;
        (* Require manual reset via SystemEnable toggle after fault clears *)
        IF NOT bSystemEnable AND NOT bFireAlarm AND bEmergencyStop THEN
            bSystemFault := FALSE;
            iControlState := 0;
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
