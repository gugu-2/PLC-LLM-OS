import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Advanced Cryogenic Liquid Argon Time Projection Chamber (LArTPC) Neutrino Detector**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 10-kiloton ultra-high purity argon circulation, multi-megawatt high-voltage electron drift field generation, and cryogenic avalanche electron multiplier arrays). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_LArTPC_NeutrinoDetector\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Advanced Cryogenic Liquid Argon Time Projection Chamber (LArTPC) Neutrino Detector

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_LArTPC_MainControl
(* 
=============================================================================
Block Name: FB_LArTPC_MainControl
Description: Advanced Cryogenic Liquid Argon Time Projection Chamber (LArTPC) 
             Neutrino Detector Control system. Manages 10-kiloton ultra-high 
             purity argon circulation, multi-megawatt high-voltage electron 
             drift field generation, and safety interlock sequencing.
Author: Elite Synthetic Data Architect (40+ years experience)
Version: 1.0.0
=============================================================================
*)
VAR_INPUT
    (* Required Physical Inputs *)
    bEnableSys            : BOOL;   (* Master System Enable from SCADA *)
    bEStopSafetyRelay     : BOOL;   (* Hardwired safety stop ok (TRUE = Healthy) *)
    rLArLevel             : REAL;   (* Liquid Argon fill level % (0.0 - 100.0) *)
    rLArTempK             : REAL;   (* Liquid Argon Temperature in Kelvin *)
    rLArPurityPpt         : REAL;   (* LAr Purity (Electro-negative contaminants) in ppt *)
    rHVDriftSetV          : REAL;   (* High Voltage Drift Setpoint (kV) *)
    rHVDriftReadV         : REAL;   (* High Voltage Drift Readback (kV) *)
    bPurificationPumpOk   : BOOL;   (* Cryogenic purification pump running status *)
    bAvalancheMultipliers : BOOL;   (* Avalanche electron multiplier array health OK *)
END_VAR
VAR_OUTPUT
    (* Required Physical Outputs *)
    bSystemReady          : BOOL;   (* Detector is fully stabilized and ready for physics data acquisition *)
    bHVEnabled            : BOOL;   (* High Voltage Drift Power Supply Active *)
    rLArCoolingValve      : REAL;   (* 0-100% cooling valve command to maintain cryo temps *)
    rPurificationFlowRate : REAL;   (* Recirculation flow rate command to purification system (L/min) *)
    bPurityAlarm          : BOOL;   (* Contaminant level above operational threshold *)
    bTempAlarm            : BOOL;   (* Argon temperature out of acceptable liquid phase bounds *)
    bCriticalFault        : BOOL;   (* E-Stop or Critical failure active (System Safed) *)
    iDetectorState        : INT;    (* Current Operational State Machine Step *)
END_VAR
VAR
    (* Internal State and Timers *)
    iState                : INT := 0; 
    tStabilization        : TON;
    tHVRamp               : TON;
    tFilterDegradation    : TON;
    
    (* Cryogenic Temperature PID Control Variables *)
    rTempError            : REAL;
    rTempIntegral         : REAL := 0.0;
    rTempProportional     : REAL;
    rTempDerivative       : REAL;
    rTempPrevError        : REAL := 0.0;
    rTempPIDOutput        : REAL;
    
    (* PID Tuning Parameters for 10-Kiloton Thermal Mass *)
    rKp                   : REAL := 12.5; 
    rKi                   : REAL := 0.05; 
    rKd                   : REAL := 5.0;  
    
    rTargetTempK          : REAL := 87.25; (* Optimal LAr phase temperature *)
    rHVErrorAbs           : REAL;
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety Interlocks and Critical Fault Evaluation *)
IF NOT bEStopSafetyRelay OR NOT bAvalancheMultipliers THEN
    bSystemReady   := FALSE;
    bHVEnabled     := FALSE;
    bCriticalFault := TRUE;
    
    (* Fail-safe state: Max cooling to prevent boil-off, stop flow to isolate *)
    rLArCoolingValve := 100.0; 
    rPurificationFlowRate := 0.0;
    
    iState := 99; (* Transition to fault state *)
    iDetectorState := iState;
    RETURN;
END_IF;

bCriticalFault := FALSE;

(* 2. Cryogenic Temperature Monitoring and PID Control *)
(* LAr exists as liquid between ~83.8K (triple point) and 87.3K at 1 atm *)
IF rLArTempK > 88.5 THEN
    (* Severe over-temp, phase change risk (boiling) *)
    bTempAlarm := TRUE;
    rLArCoolingValve := 100.0; (* Full cooling *)
ELSIF rLArTempK < 84.0 THEN
    (* Severe under-temp, freezing risk (solid argon) *)
    bTempAlarm := TRUE;
    rLArCoolingValve := 0.0;   (* Secure cooling *)
ELSE
    bTempAlarm := FALSE;
    
    (* Active PID Control for precise thermal stability *)
    rTempError := rLArTempK - rTargetTempK; 
    
    rTempProportional := rKp * rTempError;
    rTempIntegral := rTempIntegral + (rKi * rTempError);
    
    (* Anti-windup for integral term *)
    IF rTempIntegral > 100.0 THEN rTempIntegral := 100.0; END_IF;
    IF rTempIntegral < 0.0 THEN rTempIntegral := 0.0; END_IF;
    
    rTempDerivative := rKd * (rTempError - rTempPrevError);
    rTempPrevError := rTempError;
    
    rTempPIDOutput := rTempProportional + rTempIntegral + rTempDerivative;
    
    (* Clamp output to valve limits (0-100%) *)
    IF rTempPIDOutput > 100.0 THEN 
        rTempPIDOutput := 100.0; 
    ELSIF rTempPIDOutput < 0.0 THEN 
        rTempPIDOutput := 0.0; 
    END_IF;
    
    rLArCoolingValve := rTempPIDOutput;
END_IF;

(* 3. Argon Purity Monitoring (Electro-negative contamination causes electron attenuation) *)
IF rLArPurityPpt > 150.0 OR NOT bPurificationPumpOk THEN
    bPurityAlarm := TRUE;
    rPurificationFlowRate := 500.0; (* Max emergency circulation to molecular sieves *)
ELSE
    bPurityAlarm := FALSE;
    rPurificationFlowRate := 150.0; (* Nominal steady-state circulation *)
END_IF;

(* 4. Main Detector Operational State Machine *)
CASE iState OF
    0: (* IDLE / STANDBY *)
        bSystemReady := FALSE;
        bHVEnabled   := FALSE;
        tStabilization(IN := FALSE);
        tHVRamp(IN := FALSE);
        
        (* Conditions to begin startup sequence: 
           Enabled, Temps nominal, Purity nominal, Vessel full *)
        IF bEnableSys AND NOT bTempAlarm AND NOT bPurityAlarm AND (rLArLevel >= 99.5) THEN
            iState := 10;
        END_IF;

    10: (* PURIFICATION & THERMAL STABILIZATION *)
        (* Require 60 minutes (simulated 5s for testing) of thermal equilibrium *)
        tStabilization(IN := TRUE, PT := T#5S); 
        
        IF bTempAlarm OR bPurityAlarm THEN
            tStabilization(IN := FALSE);
            iState := 0; (* Abort stabilization *)
        ELSIF tStabilization.Q THEN
            tStabilization(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* HIGH VOLTAGE RAMPING *)
        (* Engage multi-megawatt drift field power supplies *)
        bHVEnabled := TRUE;
        rHVErrorAbs := ABS(rHVDriftSetV - rHVDriftReadV);
        
        (* Check if HV has reached target setpoint within 1 kV tolerance *)
        IF rHVErrorAbs < 1.0 THEN
            tHVRamp(IN := TRUE, PT := T#10S); (* Dwell to allow field to settle *)
            IF tHVRamp.Q THEN
                tHVRamp(IN := FALSE);
                iState := 30;
            END_IF;
        ELSE
            tHVRamp(IN := FALSE);
        END_IF;
        
        IF NOT bEnableSys OR bTempAlarm OR bPurityAlarm THEN
            iState := 0;
        END_IF;

    30: (* DATA ACQUISITION READY (PHYSICS RUN) *)
        bSystemReady := TRUE;
        
        (* Drop out of physics mode if any parameter deviates significantly *)
        rHVErrorAbs := ABS(rHVDriftSetV - rHVDriftReadV);
        IF NOT bEnableSys OR bTempAlarm OR bPurityAlarm OR (rHVErrorAbs > 5.0) THEN
            bSystemReady := FALSE;
            iState := 0;
        END_IF;

    99: (* FAULT RECOVERY WAIT *)
        (* Wait for E-Stop and Multiplier faults to clear before resetting to IDLE *)
        IF bEStopSafetyRelay AND bAvalancheMultipliers THEN
            iState := 0;
        END_IF;
END_CASE;

(* Update Output State Tracker *)
iDetectorState := iState;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
