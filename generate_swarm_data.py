import json, uuid, os
os.makedirs("data/swarm_raw", exist_ok=True)
prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Gigafactory Lithium-Ion Battery Slurry Coating & Drying Line**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., micro-meter cathode/anode thickness tolerance control, differential multizone drying temperature cascading, web tensioning, and solvent NMP recovery loop control). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_BatterySlurryCoating\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Gigafactory Lithium-Ion Battery Slurry Coating & Drying Line

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""
code = """```iec-st
FUNCTION_BLOCK FB_LiIonBatteryCoatingAndDrying
VAR_INPUT
    (* High-precision process physical inputs *)
    bSystemEnable           : BOOL;     (* Main safety-interlocked system enable *)
    bEmergencyStop          : BOOL;     (* E-Stop safety loop feedback (Normally Closed) *)
    rWebSpeedSetPoint       : REAL;     (* Requested line speed in m/min (0.0 - 100.0) *)
    rWebTensionFeedFwd      : REAL;     (* Web tension feedforward reference signal (N) *)
    rSlurryDensity          : REAL;     (* Measured slurry density from Coriolis meter (g/cm^3) *)
    rAnodeThicknessPV       : REAL;     (* Real-time laser thickness measurement (microns) *)
    rCathodeThicknessPV     : REAL;     (* Real-time laser thickness measurement (microns) *)
    rZone1TempPV            : REAL;     (* Multi-zone dryer Zone 1 temperature (deg C) *)
    rZone2TempPV            : REAL;     (* Multi-zone dryer Zone 2 temperature (deg C) *)
    rZone3TempPV            : REAL;     (* Multi-zone dryer Zone 3 temperature (deg C) *)
    rNMPConcentration       : REAL;     (* Solvent (NMP) vapor concentration (LEL %) *)
END_VAR

VAR_OUTPUT
    (* High-precision control actuators and state outputs *)
    bSystemReady            : BOOL;     (* Indication that all interlocks and warm-ups are met *)
    bCoatingActive          : BOOL;     (* Indication that slot die coating is engaged *)
    rSlotDiePumpSpeedCV     : REAL;     (* Commanded speed for positive displacement pump (%) *)
    rWebDriveSpeedCV        : REAL;     (* Commanded speed for master nip drive (%) *)
    rDryingHeatOutputCV     : ARRAY[1..3] OF REAL; (* PID heat outputs for multizone dryer (0-100%) *)
    bExhaustFanEnable       : BOOL;     (* Active exhaust for NMP recovery loop *)
    bCriticalAlarm          : BOOL;     (* Latched critical fault requiring intervention *)
END_VAR

VAR
    (* Internal state tracking and advanced control parameters *)
    iState                  : INT := 0; 
    
    (* Coating thickness cascade PID controllers - Simplified representations *)
    rThicknessError         : REAL;
    rThicknessIntegral      : REAL := 0.0;
    rThicknessDerivative    : REAL;
    rThicknessPrevError     : REAL := 0.0;
    rKp_Coating             : REAL := 2.5;
    rKi_Coating             : REAL := 0.05;
    rKd_Coating             : REAL := 0.1;
    
    (* Temperature Control State *)
    rTempSetPoints          : ARRAY[1..3] OF REAL := [90.0, 110.0, 130.0];
    rTempErrors             : ARRAY[1..3] OF REAL;
    rKp_Temp                : REAL := 5.0;
    
    (* Timers and diagnostics *)
    tWarmUpTimer            : TON;
    tSafetyPurgeTimer       : TON;
    tPurgeTime              : TIME := T#30S;
    
    (* NMP Solvent Safety LEL thresholds *)
    rLEL_WarningThreshold   : REAL := 25.0;
    rLEL_CriticalThreshold  : REAL := 40.0;
    
    iZone                   : INT;
END_VAR

(* === MAIN SAFETY AND INTERLOCK LOGIC === *)
IF NOT bEmergencyStop THEN
    (* Fail-safe state enforcement upon E-Stop break *)
    bSystemReady := FALSE;
    bCoatingActive := FALSE;
    rSlotDiePumpSpeedCV := 0.0;
    rWebDriveSpeedCV := 0.0;
    rDryingHeatOutputCV[1] := 0.0;
    rDryingHeatOutputCV[2] := 0.0;
    rDryingHeatOutputCV[3] := 0.0;
    bExhaustFanEnable := TRUE; (* Keep exhaust running during E-stop for solvent removal *)
    bCriticalAlarm := TRUE;
    iState := 999; (* Fault state *)
    RETURN;
END_IF;

(* Continuous solvent NMP vapor concentration check *)
IF rNMPConcentration > rLEL_CriticalThreshold THEN
    bCriticalAlarm := TRUE;
    bCoatingActive := FALSE;
    rSlotDiePumpSpeedCV := 0.0;
    bExhaustFanEnable := TRUE;
    iState := 999;
    RETURN;
END_IF;

(* === MAIN STATE MACHINE === *)
CASE iState OF
    0: (* IDLE & SYSTEM PURGE *)
        bSystemReady := FALSE;
        bCoatingActive := FALSE;
        bExhaustFanEnable := TRUE;
        rSlotDiePumpSpeedCV := 0.0;
        
        IF bSystemEnable THEN
            tSafetyPurgeTimer(IN := TRUE, PT := tPurgeTime);
            IF tSafetyPurgeTimer.Q THEN
                tSafetyPurgeTimer(IN := FALSE);
                iState := 10;
            END_IF;
        ELSE
            tSafetyPurgeTimer(IN := FALSE);
        END_IF;

    10: (* HEATING WARM-UP *)
        (* Simple proportional control for 3 zones *)
        rTempErrors[1] := rTempSetPoints[1] - rZone1TempPV;
        rTempErrors[2] := rTempSetPoints[2] - rZone2TempPV;
        rTempErrors[3] := rTempSetPoints[3] - rZone3TempPV;
        
        FOR iZone := 1 TO 3 DO
            IF rTempErrors[iZone] > 0.0 THEN
                rDryingHeatOutputCV[iZone] := rTempErrors[iZone] * rKp_Temp;
                IF rDryingHeatOutputCV[iZone] > 100.0 THEN
                    rDryingHeatOutputCV[iZone] := 100.0;
                END_IF;
            ELSE
                rDryingHeatOutputCV[iZone] := 0.0;
            END_IF;
        END_FOR;
        
        (* Transition when within 2 degrees of target *)
        IF (ABS(rTempErrors[1]) < 2.0) AND (ABS(rTempErrors[2]) < 2.0) AND (ABS(rTempErrors[3]) < 2.0) THEN
            iState := 20;
        END_IF;

        IF NOT bSystemEnable THEN
            iState := 0;
        END_IF;

    20: (* READY TO COAT *)
        bSystemReady := TRUE;
        
        (* In a real setup, operator interface triggers run mode. Here we auto-transition based on setpoint *)
        IF rWebSpeedSetPoint > 5.0 THEN
            iState := 30;
        END_IF;

        IF NOT bSystemEnable THEN
            iState := 0;
        END_IF;

    30: (* ACTIVE COATING / RUNNING *)
        bCoatingActive := TRUE;
        rWebDriveSpeedCV := rWebSpeedSetPoint;
        
        (* Slurry pump speed calculation with PID overlay for thickness control (simplified) *)
        rThicknessError := 150.0 - rAnodeThicknessPV; (* Example 150 micron target *)
        rThicknessIntegral := rThicknessIntegral + rThicknessError;
        rThicknessDerivative := rThicknessError - rThicknessPrevError;
        
        rSlotDiePumpSpeedCV := (rWebSpeedSetPoint * 0.8) + (* Feedforward based on web speed *)
                               (rKp_Coating * rThicknessError) + 
                               (rKi_Coating * rThicknessIntegral) + 
                               (rKd_Coating * rThicknessDerivative);
                               
        rThicknessPrevError := rThicknessError;
        
        (* Constrain output *)
        IF rSlotDiePumpSpeedCV > 100.0 THEN rSlotDiePumpSpeedCV := 100.0; END_IF;
        IF rSlotDiePumpSpeedCV < 0.0 THEN rSlotDiePumpSpeedCV := 0.0; END_IF;
        
        (* Ongoing multizone temperature control *)
        rTempErrors[1] := rTempSetPoints[1] - rZone1TempPV;
        rTempErrors[2] := rTempSetPoints[2] - rZone2TempPV;
        rTempErrors[3] := rTempSetPoints[3] - rZone3TempPV;
        
        FOR iZone := 1 TO 3 DO
            IF rTempErrors[iZone] > 0.0 THEN
                rDryingHeatOutputCV[iZone] := rTempErrors[iZone] * rKp_Temp;
            ELSE
                rDryingHeatOutputCV[iZone] := 0.0;
            END_IF;
        END_FOR;
        
        IF rWebSpeedSetPoint <= 1.0 THEN
            bCoatingActive := FALSE;
            rSlotDiePumpSpeedCV := 0.0;
            iState := 20;
        END_IF;

        IF NOT bSystemEnable THEN
            iState := 0;
        END_IF;
        
    999: (* FAULT / ALARM LATCHED *)
        (* Wait for manual reset sequence (simulated by E-Stop being healthy and System Enable toggled off) *)
        IF bEmergencyStop AND NOT bSystemEnable AND (rNMPConcentration < rLEL_WarningThreshold) THEN
            bCriticalAlarm := FALSE;
            iState := 0;
        END_IF;
        
END_CASE;

END_FUNCTION_BLOCK
```"""
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
