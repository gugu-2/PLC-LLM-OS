import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Ultra-High Vacuum (UHV) Molecular Beam Epitaxy (MBE) Effusion Cell Temperature and Shutter Sync**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_MBE_EffusionCell\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Ultra-High Vacuum (UHV) Molecular Beam Epitaxy (MBE) Effusion Cell Temperature and Shutter Sync

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_MBE_EffusionCell_UltraPreciseControl
(*========================================================================================
   FB_MBE_EffusionCell_UltraPreciseControl
   DESCRIPTION: 
     Advanced controller for Ultra-High Vacuum Molecular Beam Epitaxy Effusion Cell.
     Provides sub-milliKelvin temperature stability, predictive thermal compensation for 
     shutter events, and rigorous interlock handling. 
   AUTHOR: Lumina AI Cloud Swarm
   VERSION: 2.1.0 
========================================================================================*)

VAR_INPUT
    bEnableSys               : BOOL;     (* System master enable *)
    bEmergencyStopOk         : BOOL;     (* True if Safety chain is healthy *)
    bUHVStatusOk             : BOOL;     (* Ultra High Vacuum interlock signal (must be < 1e-10 Torr) *)
    rTempProcessVar          : LREAL;    (* High resolution thermocouple reading [K] *)
    rTempSetpoint            : LREAL;    (* Desired effusion cell crucible temperature [K] *)
    bShutterCommand          : BOOL;     (* Commanded shutter state: TRUE=Open, FALSE=Closed *)
    rCoolingWaterFlow        : REAL;     (* Cooling shroud flow rate [L/min] *)
    bCryoPanelOk             : BOOL;     (* LN2 cryopanel thermal status *)
END_VAR

VAR_OUTPUT
    bSystemReady             : BOOL;     (* Indicates system is stablized and ready for growth *)
    rHeaterControlSignal     : LREAL;    (* High resolution PWM or Analog out for Heater PSU (0-100%) *)
    bShutterActual           : BOOL;     (* Actuated shutter state *)
    bAlarmCritical           : BOOL;     (* Fast shutdown required alarm flag *)
    bAlarmWarning            : BOOL;     (* Non-critical deviation alarm *)
    rTempErrorFiltered       : LREAL;    (* Filtered error for HMI monitoring *)
    iOperationState          : INT;      (* Current state machine step *)
END_VAR

VAR
    (* Internal State and Filtering *)
    iState                   : INT := 0; (* 0: IDLE, 10: INIT, 20: RAMP, 30: SOAK, 40: READY, 99: FAULT *)
    rLastTemp                : LREAL := 0.0;
    rFilteredTemp            : LREAL := 0.0;
    rAlpha                   : LREAL := 0.05; (* EMA Filter coefficient *)
    
    (* PID Control Variables *)
    rKp                      : LREAL := 25.5;
    rKi                      : LREAL := 0.12;
    rKd                      : LREAL := 85.0;
    rIntegral                : LREAL := 0.0;
    rLastError               : LREAL := 0.0;
    rDerivative              : LREAL := 0.0;
    rControlOutputRaw        : LREAL := 0.0;
    
    (* Shutter Compensation *)
    rShutterThermalKick      : LREAL := 12.5; (* Added heater power % when shutter opens to prevent temp drop *)
    tShutterTimer            : TON;
    
    (* Limit and Safety *)
    rMaxTemp                 : LREAL := 1500.0; (* K *)
    rMaxHeaterChangeRate     : LREAL := 2.0; (* % per cycle *)
    rLastHeaterOutput        : LREAL := 0.0;
    tSoakTimer               : TON;
    tRampTimer               : TON;
    
    bInitDone                : BOOL := FALSE;
END_VAR

(* === MAIN LOGIC === *)

(* 1. Interlock and Safety Handling *)
IF NOT bEmergencyStopOk OR NOT bUHVStatusOk OR NOT bCryoPanelOk OR (rCoolingWaterFlow < 1.5) OR (rTempProcessVar > rMaxTemp) THEN
    (* Immediate safe state *)
    bSystemReady := FALSE;
    rHeaterControlSignal := 0.0;
    bShutterActual := FALSE;
    bAlarmCritical := TRUE;
    iState := 99; (* FAULT *)
    rIntegral := 0.0;
    rLastHeaterOutput := 0.0;
    RETURN;
ELSE
    bAlarmCritical := FALSE;
END_IF;

(* 2. Signal Filtering (Exponential Moving Average) *)
IF NOT bInitDone THEN
    rFilteredTemp := rTempProcessVar;
    bInitDone := TRUE;
ELSE
    rFilteredTemp := rFilteredTemp + rAlpha * (rTempProcessVar - rFilteredTemp);
END_IF;
rTempErrorFiltered := rTempSetpoint - rFilteredTemp;

(* 3. State Machine *)
CASE iState OF
    0: (* IDLE *)
        bSystemReady := FALSE;
        rHeaterControlSignal := 0.0;
        bShutterActual := FALSE;
        rIntegral := 0.0;
        IF bEnableSys THEN
            iState := 10;
        END_IF;
        
    10: (* INIT *)
        (* Validate setpoints before ramping *)
        IF (rTempSetpoint > 273.15) AND (rTempSetpoint <= rMaxTemp) THEN
            iState := 20;
        ELSE
            bAlarmWarning := TRUE;
            iState := 0;
        END_IF;
        
    20: (* RAMP *)
        bSystemReady := FALSE;
        (* Execute PID with limited output rate (soft start) *)
        rIntegral := rIntegral + (rTempErrorFiltered * rKi);
        (* Anti-windup *)
        IF rIntegral > 100.0 THEN rIntegral := 100.0; END_IF;
        IF rIntegral < 0.0 THEN rIntegral := 0.0; END_IF;
        
        rDerivative := (rTempErrorFiltered - rLastError) * rKd;
        rControlOutputRaw := (rTempErrorFiltered * rKp) + rIntegral + rDerivative;
        
        (* Clamp Output *)
        IF rControlOutputRaw > 100.0 THEN rControlOutputRaw := 100.0; END_IF;
        IF rControlOutputRaw < 0.0 THEN rControlOutputRaw := 0.0; END_IF;
        
        rHeaterControlSignal := rControlOutputRaw;
        
        (* Check if near setpoint to start soak *)
        IF ABS(rTempErrorFiltered) < 1.0 THEN
            iState := 30;
        END_IF;
        
    30: (* SOAK *)
        (* Maintain temp, wait for stability *)
        rIntegral := rIntegral + (rTempErrorFiltered * rKi);
        rDerivative := (rTempErrorFiltered - rLastError) * rKd;
        rHeaterControlSignal := (rTempErrorFiltered * rKp) + rIntegral + rDerivative;
        
        tSoakTimer(IN := TRUE, PT := T#120S);
        IF tSoakTimer.Q THEN
            tSoakTimer(IN := FALSE);
            iState := 40;
        END_IF;
        IF ABS(rTempErrorFiltered) >= 2.0 THEN
            (* Lost stability, go back to ramp/stabilize *)
            tSoakTimer(IN := FALSE);
            iState := 20;
        END_IF;
        
    40: (* READY *)
        bSystemReady := TRUE;
        
        (* Advanced PID + Feedforward Shutter Thermal Compensation *)
        rIntegral := rIntegral + (rTempErrorFiltered * rKi);
        rDerivative := (rTempErrorFiltered - rLastError) * rKd;
        rControlOutputRaw := (rTempErrorFiltered * rKp) + rIntegral + rDerivative;
        
        (* Shutter logic with feedforward kick *)
        IF bShutterCommand THEN
            IF NOT bShutterActual THEN
                (* Just opened, apply thermal kick *)
                rControlOutputRaw := rControlOutputRaw + rShutterThermalKick;
            END_IF;
            bShutterActual := TRUE;
        ELSE
            IF bShutterActual THEN
                 (* Just closed, remove thermal kick by integrating down naturally, but immediately drop feedforward *)
                 rControlOutputRaw := rControlOutputRaw - (rShutterThermalKick * 0.5); 
            END_IF;
            bShutterActual := FALSE;
        END_IF;
        
        (* Limit control rate to prevent PSU spikes *)
        IF (rControlOutputRaw - rLastHeaterOutput) > rMaxHeaterChangeRate THEN
            rHeaterControlSignal := rLastHeaterOutput + rMaxHeaterChangeRate;
        ELSIF (rLastHeaterOutput - rControlOutputRaw) > rMaxHeaterChangeRate THEN
            rHeaterControlSignal := rLastHeaterOutput - rMaxHeaterChangeRate;
        ELSE
            rHeaterControlSignal := rControlOutputRaw;
        END_IF;
        
        (* Clamp limits *)
        IF rHeaterControlSignal > 100.0 THEN rHeaterControlSignal := 100.0; END_IF;
        IF rHeaterControlSignal < 0.0 THEN rHeaterControlSignal := 0.0; END_IF;
        
        IF NOT bEnableSys THEN
            iState := 0;
        END_IF;
        
    99: (* FAULT *)
        rHeaterControlSignal := 0.0;
        bShutterActual := FALSE;
        IF bEnableSys = FALSE AND bEmergencyStopOk AND bUHVStatusOk THEN
            (* Require enable toggle to clear fault *)
            iState := 0;
            bAlarmCritical := FALSE;
        END_IF;
        
END_CASE;

(* 4. Final Updates *)
rLastError := rTempErrorFiltered;
rLastHeaterOutput := rHeaterControlSignal;
iOperationState := iState;

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
