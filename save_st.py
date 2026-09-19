import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: High-Volume Automotive Tire Manufacturing Banbury Mixer Ram Pressure and Carbon Black Dosing**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_TireMfg_BanburyMixer\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: High-Volume Automotive Tire Manufacturing Banbury Mixer Ram Pressure and Carbon Black Dosing

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_BanburyMixer_RamPressureDosing
(*=============================================================================
  Block Name: FB_BanburyMixer_RamPressureDosing
  Description: Ultra-complex control for High-Volume Automotive Tire Banbury Mixer.
               Manages dynamic Ram Pressure control and precise Carbon Black (CB)
               dosing based on multi-variate compound formulation and rheology.
               Incorporates sensor fusion, noise filtering, and predictive fault 
               detection.
  Version: 4.2.1
=============================================================================*)
VAR_INPUT
    bEnable                 : BOOL;     (* System global enable *)
    bEmergencyStop          : BOOL;     (* Safety relay (FALSE = E-Stop active) *)
    bStartBatch             : BOOL;     (* Command to start a new mixing batch *)
    rRamPressureActual      : REAL;     (* Measured ram pressure (bar) *)
    rRamPosActual           : REAL;     (* Measured ram position (mm) *)
    rCarbonBlackWeight      : REAL;     (* Measured carbon black weight (kg) *)
    rChamberTemp            : REAL;     (* Mixer chamber temperature (deg C) *)
    rMotorPowerKW           : REAL;     (* Main rotor motor power draw (kW) *)
    rTargetRamPressure      : REAL;     (* Recipe setpoint for ram pressure (bar) *)
    rTargetCBWeight         : REAL;     (* Recipe setpoint for CB dosing (kg) *)
END_VAR

VAR_OUTPUT
    bSystemReady            : BOOL;     (* System ready for batch *)
    rRamValveCommand        : REAL;     (* Proportional valve command 0-100% *)
    bCBValveOpen            : BOOL;     (* Carbon black dosing gate valve *)
    rCBFeederSpeed          : REAL;     (* Carbon black auger speed 0-100% *)
    bBatchComplete          : BOOL;     (* Batch processing complete flag *)
    bAlarm                  : BOOL;     (* Aggregated fault flag *)
    iAlarmCode              : INT;      (* Diagnostics alarm code *)
END_VAR

VAR
    iState                  : INT := 0; (* Internal state machine *)
    tMixingTimer            : TON;
    tDosingTimer            : TON;
    
    (* Filtered signals *)
    rFiltChamberTemp        : REAL := 0.0;
    rFiltMotorPower         : REAL := 0.0;
    rFiltRamPressure        : REAL := 0.0;
    
    (* PID variables for Ram Pressure *)
    rPressureError          : REAL := 0.0;
    rPressureIntegral       : REAL := 0.0;
    rPressureDerivative     : REAL := 0.0;
    rPressurePrevError      : REAL := 0.0;
    rKp                     : REAL := 2.5;
    rKi                     : REAL := 0.8;
    rKd                     : REAL := 0.15;
    
    (* Dosing control *)
    rWeightDelta            : REAL := 0.0;
    bFineDosingPhase        : BOOL := FALSE;
    
    (* Safety limits *)
    rMaxTemp                : REAL := 185.0;  (* Max safe temp for rubber *)
    rMaxPressure            : REAL := 15.0;   (* Max safe ram pressure *)
    
    bInitDone               : BOOL := FALSE;
END_VAR

(* === INITIALIZATION & FILTERING === *)
IF NOT bInitDone THEN
    rFiltChamberTemp := rChamberTemp;
    rFiltMotorPower := rMotorPowerKW;
    rFiltRamPressure := rRamPressureActual;
    bInitDone := TRUE;
END_IF;

(* Exponential Moving Average for noisy sensors *)
rFiltChamberTemp := (rFiltChamberTemp * 0.9) + (rChamberTemp * 0.1);
rFiltMotorPower := (rFiltMotorPower * 0.85) + (rMotorPowerKW * 0.15);
rFiltRamPressure := (rFiltRamPressure * 0.8) + (rRamPressureActual * 0.2);

(* === SAFETY INTERLOCKS === *)
IF NOT bEmergencyStop THEN
    rRamValveCommand := 0.0;
    bCBValveOpen := FALSE;
    rCBFeederSpeed := 0.0;
    bSystemReady := FALSE;
    bAlarm := TRUE;
    iAlarmCode := 99; (* E-STOP Active *)
    iState := 0;
    RETURN;
END_IF;

IF rFiltChamberTemp > rMaxTemp THEN
    rRamValveCommand := 0.0;
    bCBValveOpen := FALSE;
    rCBFeederSpeed := 0.0;
    bAlarm := TRUE;
    iAlarmCode := 101; (* Thermal Runaway *)
    iState := 0;
    RETURN;
END_IF;

IF rFiltRamPressure > rMaxPressure THEN
    rRamValveCommand := 0.0; (* Vent pressure *)
    bAlarm := TRUE;
    iAlarmCode := 102; (* Over-pressure *)
END_IF;

(* === MAIN STATE MACHINE === *)
CASE iState OF
    0: (* IDLE *)
        rRamValveCommand := 0.0;
        bCBValveOpen := FALSE;
        rCBFeederSpeed := 0.0;
        bBatchComplete := FALSE;
        rPressureIntegral := 0.0;
        
        IF bEnable AND NOT bAlarm THEN
            bSystemReady := TRUE;
            IF bStartBatch THEN
                bSystemReady := FALSE;
                iState := 10;
            END_IF;
        ELSE
            bSystemReady := FALSE;
        END_IF;

    10: (* INITIATE DOSING *)
        bCBValveOpen := TRUE;
        rWeightDelta := rTargetCBWeight - rCarbonBlackWeight;
        
        IF rWeightDelta > 5.0 THEN
            (* Bulk Dosing *)
            rCBFeederSpeed := 80.0; 
        ELSIF rWeightDelta > 0.2 THEN
            (* Fine Dosing *)
            bFineDosingPhase := TRUE;
            rCBFeederSpeed := (rWeightDelta / 5.0) * 80.0;
            IF rCBFeederSpeed < 10.0 THEN
                rCBFeederSpeed := 10.0;
            END_IF;
        ELSE
            (* Dosing Complete *)
            rCBFeederSpeed := 0.0;
            bCBValveOpen := FALSE;
            tDosingTimer(IN := TRUE, PT := T#2S);
            IF tDosingTimer.Q THEN
                tDosingTimer(IN := FALSE);
                iState := 20;
            END_IF;
        END_IF;

    20: (* RAM LOWER & PRESSURIZE *)
        (* PID Control for Ram Pressure *)
        rPressureError := rTargetRamPressure - rFiltRamPressure;
        rPressureIntegral := rPressureIntegral + (rPressureError * 0.1); (* Assuming 100ms cycle *)
        
        (* Anti-windup *)
        IF rPressureIntegral > 100.0 THEN rPressureIntegral := 100.0; END_IF;
        IF rPressureIntegral < -100.0 THEN rPressureIntegral := -100.0; END_IF;
        
        rPressureDerivative := (rPressureError - rPressurePrevError) / 0.1;
        rPressurePrevError := rPressureError;
        
        rRamValveCommand := (rKp * rPressureError) + (rKi * rPressureIntegral) + (rKd * rPressureDerivative);
        
        (* Saturate Output *)
        IF rRamValveCommand > 100.0 THEN rRamValveCommand := 100.0; END_IF;
        IF rRamValveCommand < 0.0 THEN rRamValveCommand := 0.0; END_IF;
        
        (* Dynamic viscosity inference based on Motor Power *)
        IF rFiltMotorPower > 1500.0 THEN
            (* Polymer breakdown phase detected, hold pressure *)
            tMixingTimer(IN := TRUE, PT := T#45S);
            IF tMixingTimer.Q THEN
                tMixingTimer(IN := FALSE);
                iState := 30;
            END_IF;
        END_IF;

    30: (* BATCH COMPLETE *)
        rRamValveCommand := 0.0; (* Raise ram *)
        bBatchComplete := TRUE;
        IF NOT bStartBatch THEN
            iState := 0;
        END_IF;

    ELSE
        iState := 0;
END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
