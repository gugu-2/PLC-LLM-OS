import json, uuid
import os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial Scale Offshore Aquaculture Open-Ocean Submersible Pen**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Automated dead-fish extraction airlift, hyperbaric multi-chamber buoyancy dynamic leveling, and storm-surge adaptive mooring tensioning). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_SubmersibleAquaculturePen\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Scale Offshore Aquaculture Open-Ocean Submersible Pen

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_OffshoreAquaculturePen_Controller
(*
    ====================================================================
    FB_OffshoreAquaculturePen_Controller
    Author: Lumina AI Cloud Swarm (40+ Yr Automation Architect)
    Domain: Industrial Scale Offshore Aquaculture Open-Ocean Submersible Pen
    Description: 
        Advanced control for automated dead-fish extraction airlift,
        hyperbaric multi-chamber buoyancy dynamic leveling, and 
        storm-surge adaptive mooring tensioning.
        Includes advanced PID/state-machine resilience, multi-layered 
        safety interlocks, and sensor noise filtering (EMA filters).
    ====================================================================
*)

VAR_INPUT
    bSystemEnable           : BOOL;     (* System master enable signal *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal (Active HIGH = OK) *)
    
    (* Environmental & Motion Sensors *)
    rWaveHeight_m           : REAL;     (* Current wave height in meters from acoustic doppler *)
    rWaterCurrent_kts       : REAL;     (* Water current speed in knots *)
    rDepthTarget_m          : REAL;     (* Target submergence depth in meters *)
    rDepthCurrent_m         : REAL;     (* Actual submergence depth in meters *)
    rPitchAngle_deg         : REAL;     (* Pen pitch angle in degrees *)
    rRollAngle_deg          : REAL;     (* Pen roll angle in degrees *)
    
    (* Mooring & Airlift Sensors *)
    rMooringTensionN        : ARRAY[1..4] OF REAL; (* Tension on 4 main mooring lines in Newtons *)
    bDeadFishAccumDetected  : BOOL;     (* Optical/Sonar trigger for dead-fish at bottom cone *)
    rAirSupplyPress_bar     : REAL;     (* Compressed air supply pressure in bar *)
END_VAR

VAR_OUTPUT
    bSystemReady            : BOOL;     (* System ready status indicator *)
    bStormModeActive        : BOOL;     (* True if storm surge protection is active *)
    
    (* Actuator Commands *)
    rBuoyancyValveCmd       : ARRAY[1..4] OF REAL; (* 0.0 to 100.0% command for quadrant buoyancy valves *)
    rWinchTensionCmdN       : ARRAY[1..4] OF REAL; (* Target tension for 4 mooring winches in Newtons *)
    bAirliftPumpEnable      : BOOL;     (* Enable signal for dead fish airlift extraction pump *)
    rAirliftAirFlowCmd_Lpm  : REAL;     (* Airlift air injection flow rate in Liters per min *)
    
    bCriticalAlarm          : BOOL;     (* Fault alarm output - immediate intervention required *)
    iErrorCode              : INT;      (* Diagnostics error code *)
END_VAR

VAR
    (* Internal State Machine *)
    iMainState              : INT := 0; (* 0:Init, 10:Idle, 20:Submerge/Surface, 30:StormMode, 40:AirliftExtraction, 99:Fault *)
    
    (* Sensor Filters (EMA) *)
    rWaveHeightFiltered     : REAL := 0.0;
    rDepthFiltered          : REAL := 0.0;
    
    (* PID & Control Variables *)
    rDepthError             : REAL;
    rDepthIntegral          : REAL := 0.0;
    rBuoyancyBaseOutput     : REAL;
    
    (* Timers & Triggers *)
    tAirliftTimer           : TON;
    tStormSurgeTimer        : TON;
    rMaxTensionLimit        : REAL := 500000.0; (* 500 kN max safe tension *)
    
    i                       : INT;
    bTensionFault           : BOOL;
END_VAR

(* === MAIN LOGIC === *)

(* 1. Safety & Interlocks *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bAirliftPumpEnable := FALSE;
    FOR i := 1 TO 4 DO
        rBuoyancyValveCmd[i] := 0.0;
        rWinchTensionCmdN[i] := rMooringTensionN[i]; (* Lock winches at current tension *)
    END_FOR;
    bCriticalAlarm := TRUE;
    iErrorCode := 1001; (* E-STOP Active *)
    iMainState := 99;
    RETURN;
END_IF;

IF rAirSupplyPress_bar < 5.0 THEN
    bCriticalAlarm := TRUE;
    iErrorCode := 1002; (* Low Air Supply *)
    iMainState := 99;
END_IF;

(* 2. Signal Processing (EMA Filtering to reject sensor noise) *)
rWaveHeightFiltered := (0.1 * rWaveHeight_m) + (0.9 * rWaveHeightFiltered);
rDepthFiltered := (0.05 * rDepthCurrent_m) + (0.95 * rDepthFiltered);

(* 3. Mooring Tension Monitoring *)
bTensionFault := FALSE;
FOR i := 1 TO 4 DO
    IF rMooringTensionN[i] > rMaxTensionLimit THEN
        bTensionFault := TRUE;
    END_IF;
END_FOR;

IF bTensionFault THEN
    bCriticalAlarm := TRUE;
    iErrorCode := 1003; (* Mooring Tension Overload *)
    iMainState := 99;
END_IF;

(* 4. State Machine Control *)
CASE iMainState OF
    0: (* INIT *)
        bSystemReady := FALSE;
        bStormModeActive := FALSE;
        bAirliftPumpEnable := FALSE;
        IF bSystemEnable AND NOT bCriticalAlarm THEN
            iMainState := 10;
        END_IF;

    10: (* IDLE & NORMAL LEVELING *)
        bSystemReady := TRUE;
        bStormModeActive := FALSE;
        
        (* Check for Storm conditions *)
        IF rWaveHeightFiltered > 4.5 OR rWaterCurrent_kts > 3.0 THEN
            tStormSurgeTimer(IN := TRUE, PT := T#10S);
            IF tStormSurgeTimer.Q THEN
                iMainState := 30;
                tStormSurgeTimer(IN := FALSE);
            END_IF;
        ELSE
            tStormSurgeTimer(IN := FALSE);
        END_IF;
        
        (* Check for Dead Fish Airlift Requirement *)
        IF bDeadFishAccumDetected AND rAirSupplyPress_bar >= 6.0 THEN
            iMainState := 40;
        END_IF;
        
        (* Basic Depth PID Calculation *)
        rDepthError := rDepthTarget_m - rDepthFiltered;
        rDepthIntegral := rDepthIntegral + (rDepthError * 0.1);
        
        (* Anti-windup *)
        IF rDepthIntegral > 100.0 THEN rDepthIntegral := 100.0; END_IF;
        IF rDepthIntegral < -100.0 THEN rDepthIntegral := -100.0; END_IF;
        
        rBuoyancyBaseOutput := (rDepthError * 5.0) + (rDepthIntegral * 0.5);
        
        (* Distribute buoyancy to maintain level (Pitch/Roll compensation) *)
        rBuoyancyValveCmd[1] := rBuoyancyBaseOutput + (rPitchAngle_deg * 2.0) + (rRollAngle_deg * 2.0);
        rBuoyancyValveCmd[2] := rBuoyancyBaseOutput + (rPitchAngle_deg * 2.0) - (rRollAngle_deg * 2.0);
        rBuoyancyValveCmd[3] := rBuoyancyBaseOutput - (rPitchAngle_deg * 2.0) + (rRollAngle_deg * 2.0);
        rBuoyancyValveCmd[4] := rBuoyancyBaseOutput - (rPitchAngle_deg * 2.0) - (rRollAngle_deg * 2.0);
        
        (* Maintain nominal mooring tension *)
        FOR i := 1 TO 4 DO
            rWinchTensionCmdN[i] := 150000.0; (* 150 kN nominal *)
        END_FOR;

    30: (* STORM SURGE ADAPTIVE MODE *)
        bStormModeActive := TRUE;
        
        (* Rapidly submerge to safer target depth (e.g., 30m) *)
        rDepthError := 30.0 - rDepthFiltered;
        rBuoyancyBaseOutput := rDepthError * 8.0; (* Aggressive P-Gain *)
        
        FOR i := 1 TO 4 DO
            rBuoyancyValveCmd[i] := rBuoyancyBaseOutput;
            (* Increase mooring tension compliance for wave elasticity *)
            rWinchTensionCmdN[i] := 250000.0;
        END_FOR;
        
        (* Exit storm mode if conditions calm down *)
        IF rWaveHeightFiltered < 3.0 AND rWaterCurrent_kts < 2.0 THEN
            iMainState := 10;
        END_IF;

    40: (* DEAD FISH AIRLIFT EXTRACTION *)
        (* Maintain position while airlifting *)
        rBuoyancyBaseOutput := 50.0; 
        FOR i := 1 TO 4 DO
            rBuoyancyValveCmd[i] := rBuoyancyBaseOutput;
        END_FOR;
        
        bAirliftPumpEnable := TRUE;
        rAirliftAirFlowCmd_Lpm := 850.0; (* Optimal airlift aeration *)
        
        tAirliftTimer(IN := TRUE, PT := T#120S); (* Run for 2 minutes per cycle *)
        
        IF tAirliftTimer.Q OR NOT bDeadFishAccumDetected THEN
            tAirliftTimer(IN := FALSE);
            bAirliftPumpEnable := FALSE;
            rAirliftAirFlowCmd_Lpm := 0.0;
            iMainState := 10;
        END_IF;
        
    99: (* FAULT STATE *)
        bSystemReady := FALSE;
        bStormModeActive := FALSE;
        bAirliftPumpEnable := FALSE;
        rAirliftAirFlowCmd_Lpm := 0.0;
        
        (* Fallback safe state - surface slowly *)
        FOR i := 1 TO 4 DO
            rBuoyancyValveCmd[i] := 100.0; (* Full air blow to surface *)
        END_FOR;
        
        IF bSystemEnable = FALSE AND bEmergencyStop THEN
            bCriticalAlarm := FALSE;
            iErrorCode := 0;
            iMainState := 0; (* Reset if enable is cycled and E-Stop is clear *)
        END_IF;

END_CASE;

(* Constrain Outputs *)
FOR i := 1 TO 4 DO
    IF rBuoyancyValveCmd[i] > 100.0 THEN rBuoyancyValveCmd[i] := 100.0; END_IF;
    IF rBuoyancyValveCmd[i] < 0.0 THEN rBuoyancyValveCmd[i] := 0.0; END_IF;
END_FOR;

END_FUNCTION_BLOCK
```"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
