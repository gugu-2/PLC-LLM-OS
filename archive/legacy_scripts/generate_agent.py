import os, json, uuid

prompt = """<USER_REQUEST>
You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial Scale Vertical Farming Aeroponic Nutrient Delivery**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., High-pressure ultrasonic fogging droplet diameter regulation, multi-spectral LED photosynthetic photon flux density (PPFD) dimming, and root-zone dissolved oxygen micro-bubbling). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Aeroponic_NutrientDelivery\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Scale Vertical Farming Aeroponic Nutrient Delivery

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT.
</USER_REQUEST>"""

code = """```iec-st
FUNCTION_BLOCK FB_Aeroponic_NutrientDelivery
VAR_INPUT
    (* Core Enable & Safety *)
    bSystemEnable           : BOOL;     (* Main system enable command *)
    bEmergencyStopOk        : BOOL;     (* Safety relay OK signal, TRUE=OK *)
    
    (* Environmental Sensors *)
    rNutrientTankLevel      : REAL;     (* Nutrient tank level in % *)
    rEC_SensorVal           : REAL;     (* Electrical Conductivity reading in mS/cm *)
    rPH_SensorVal           : REAL;     (* pH value reading *)
    rDO_SensorVal           : REAL;     (* Dissolved Oxygen in mg/L *)
    
    (* Climate & Micro-environment *)
    rRootZoneTemp           : REAL;     (* Root zone temperature in deg C *)
    rAmbientRH              : REAL;     (* Ambient Relative Humidity in % *)
    rCanopyPPFD             : REAL;     (* Canopy Photosynthetic Photon Flux Density umol/m2/s *)
    rManifoldPressure       : REAL;     (* Fogging manifold pressure in bar *)
END_VAR

VAR_OUTPUT
    (* Actuators & Controls *)
    rHP_PumpSpeedCmd        : REAL;     (* High-pressure pump speed 0-100% *)
    rFoggerDutyCycle        : REAL;     (* Ultrasonic fogger PWM duty cycle 0-100% *)
    rDosingPumpA_Speed      : REAL;     (* Nutrient Part A dosing pump 0-100% *)
    rDosingPumpB_Speed      : REAL;     (* Nutrient Part B dosing pump 0-100% *)
    rPH_DownDosingSpeed     : REAL;     (* pH down dosing pump 0-100% *)
    rAirCompressorCmd       : REAL;     (* Micro-bubbling compressor 0-100% *)
    
    (* Status & Alarms *)
    bSystemReady            : BOOL;     (* TRUE when parameters stabilized & ready for cycle *)
    bActiveFogging          : BOOL;     (* TRUE when actively misting roots *)
    bCriticalAlarm          : BOOL;     (* TRUE on critical fault (low pressure, dry run) *)
    iAlarmCode              : INT;      (* Diagnostics alarm code *)
END_VAR

VAR
    (* State Machine *)
    iState                  : INT := 0; 
    iSubState               : INT := 0;
    
    (* Internal Timers & Triggers *)
    tFoggingCycleTimer      : TON;
    tDosingStabilization    : TON;
    tSafetyDelay            : TON;
    
    (* Sensor Filters & Moving Averages *)
    rFilteredEC             : REAL;
    rFilteredPH             : REAL;
    rFilteredDO             : REAL;
    
    (* PID & Control Variables *)
    rPressureError          : REAL;
    rPressureIntegral       : REAL;
    rPressureDerivative     : REAL;
    rLastPressureError      : REAL;
    
    (* Constants & Parameters *)
    rEC_Setpoint            : REAL := 1.8;   (* target 1.8 mS/cm *)
    rPH_Setpoint            : REAL := 5.8;   (* target 5.8 pH *)
    rPressureSetpoint       : REAL := 80.0;  (* target 80 bar for optimal 50um droplets *)
    
    (* Noise filter factor *)
    rAlpha                  : REAL := 0.2;   (* First-order low pass filter weight *)
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety & Interlocks *)
IF NOT bEmergencyStopOk THEN
    (* Immediate safe state on E-Stop *)
    bSystemReady := FALSE;
    bActiveFogging := FALSE;
    bCriticalAlarm := TRUE;
    iAlarmCode := 999; (* E-Stop Active *)
    
    (* Stop all actuators *)
    rHP_PumpSpeedCmd := 0.0;
    rFoggerDutyCycle := 0.0;
    rDosingPumpA_Speed := 0.0;
    rDosingPumpB_Speed := 0.0;
    rPH_DownDosingSpeed := 0.0;
    rAirCompressorCmd := 0.0;
    
    iState := 0;
    RETURN;
END_IF;

(* 2. Sensor Noise Filtering (First-Order Low Pass) *)
rFilteredEC := (rAlpha * rEC_SensorVal) + ((1.0 - rAlpha) * rFilteredEC);
rFilteredPH := (rAlpha * rPH_SensorVal) + ((1.0 - rAlpha) * rFilteredPH);
rFilteredDO := (rAlpha * rDO_SensorVal) + ((1.0 - rAlpha) * rFilteredDO);

(* 3. Alarm Monitoring *)
IF rNutrientTankLevel < 5.0 THEN
    bCriticalAlarm := TRUE;
    iAlarmCode := 101; (* Dry run protection *)
    iState := 0;
ELSIF rFilteredPH > 7.5 OR rFilteredPH < 4.0 THEN
    bCriticalAlarm := TRUE;
    iAlarmCode := 102; (* pH out of critical bounds *)
    iState := 0;
ELSE
    bCriticalAlarm := FALSE;
    iAlarmCode := 0;
END_IF;

(* 4. Main State Machine *)
CASE iState OF
    0: (* IDLE / FAULT RECOVERY *)
        bSystemReady := FALSE;
        bActiveFogging := FALSE;
        rHP_PumpSpeedCmd := 0.0;
        rFoggerDutyCycle := 0.0;
        
        IF bSystemEnable AND NOT bCriticalAlarm THEN
            tSafetyDelay(IN := TRUE, PT := T#3S);
            IF tSafetyDelay.Q THEN
                tSafetyDelay(IN := FALSE);
                iState := 10;
            END_IF;
        ELSE
            tSafetyDelay(IN := FALSE);
        END_IF;

    10: (* WATER QUALITY CORRECTION *)
        (* Micro-bubbling for DO management *)
        IF rFilteredDO < 6.0 THEN
            rAirCompressorCmd := 80.0;
        ELSE
            rAirCompressorCmd := 30.0; (* Maintenance mode *)
        END_IF;
        
        (* Dosing Control - Simplified Proportional *)
        IF rFilteredEC < (rEC_Setpoint - 0.1) THEN
            rDosingPumpA_Speed := 25.0;
            rDosingPumpB_Speed := 25.0;
        ELSE
            rDosingPumpA_Speed := 0.0;
            rDosingPumpB_Speed := 0.0;
        END_IF;
        
        IF rFilteredPH > (rPH_Setpoint + 0.2) THEN
            rPH_DownDosingSpeed := 15.0;
        ELSE
            rPH_DownDosingSpeed := 0.0;
        END_IF;
        
        (* Stabilization Timer *)
        tDosingStabilization(IN := (rDosingPumpA_Speed = 0.0 AND rPH_DownDosingSpeed = 0.0), PT := T#10S);
        IF tDosingStabilization.Q THEN
            bSystemReady := TRUE;
            iState := 20;
        END_IF;

    20: (* FOGGING CYCLE - ACTIVE *)
        IF NOT bSystemEnable THEN
            iState := 0;
        END_IF;
        
        bActiveFogging := TRUE;
        
        (* PID Control for High Pressure Pump to maintain 80 bar *)
        rPressureError := rPressureSetpoint - rManifoldPressure;
        rPressureIntegral := rPressureIntegral + (rPressureError * 0.1); (* Assuming 100ms cycle *)
        
        (* Anti-windup *)
        IF rPressureIntegral > 100.0 THEN rPressureIntegral := 100.0; END_IF;
        IF rPressureIntegral < -100.0 THEN rPressureIntegral := -100.0; END_IF;
        
        rPressureDerivative := (rPressureError - rLastPressureError) / 0.1;
        rHP_PumpSpeedCmd := (2.5 * rPressureError) + (0.5 * rPressureIntegral) + (0.1 * rPressureDerivative);
        
        IF rHP_PumpSpeedCmd > 100.0 THEN rHP_PumpSpeedCmd := 100.0; END_IF;
        IF rHP_PumpSpeedCmd < 0.0 THEN rHP_PumpSpeedCmd := 0.0; END_IF;
        
        rLastPressureError := rPressureError;
        
        (* Ultrasonic Fogger PWM Modulation based on Vapor Pressure Deficit (approximated) *)
        IF rAmbientRH < 60.0 THEN
            rFoggerDutyCycle := 90.0;
        ELSE
            rFoggerDutyCycle := 60.0;
        END_IF;
        
        (* Fogging Duration Timer *)
        tFoggingCycleTimer(IN := TRUE, PT := T#15S); (* 15 second mist burst *)
        IF tFoggingCycleTimer.Q THEN
            tFoggingCycleTimer(IN := FALSE);
            iState := 30;
        END_IF;

    30: (* FOGGING CYCLE - REST *)
        bActiveFogging := FALSE;
        rHP_PumpSpeedCmd := 0.0;
        rFoggerDutyCycle := 0.0;
        
        tFoggingCycleTimer(IN := TRUE, PT := T#5M); (* 5 minute rest to allow root oxygenation *)
        IF tFoggingCycleTimer.Q THEN
            tFoggingCycleTimer(IN := FALSE);
            IF bSystemEnable THEN
                iState := 10; (* Recheck water quality before next burst *)
            ELSE
                iState := 0;
            END_IF;
        END_IF;
        
    ELSE
        (* Invalid state trap *)
        iState := 0;
END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
