import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial Scale Yeast Fermentation Bioreactor Dissolved Oxygen and Agitator Shear Control**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Bioreactor_YeastDO\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Scale Yeast Fermentation Bioreactor Dissolved Oxygen and Agitator Shear Control

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_Bioreactor_YeastDO
VAR_INPUT
    bEnable                 : BOOL;     (* System master enable signal *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal - Active HIGH *)
    rDO_Measurement_1       : REAL;     (* Dissolved Oxygen probe 1 [%] *)
    rDO_Measurement_2       : REAL;     (* Dissolved Oxygen probe 2 [%] *)
    rAgitatorSpeed_Fdbk     : REAL;     (* Agitator actual speed [RPM] *)
    rVesselPressure         : REAL;     (* Headspace pressure [bar] *)
    bAgitatorDrive_OK       : BOOL;     (* Agitator VFD status *)
    bSpargerValve_OK        : BOOL;     (* Air sparger control valve status *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* Bioreactor control system ready *)
    rAgitatorSpeed_Cmd      : REAL;     (* Speed command to agitator VFD [RPM] *)
    rSpargerFlow_Cmd        : REAL;     (* Airflow command to sparger mass flow controller [SLPM] *)
    bAlarm_HighShear        : BOOL;     (* Excessive shear force warning *)
    bAlarm_LowDO            : BOOL;     (* Critical hypoxia warning *)
    bAlarm_SensorFault      : BOOL;     (* DO sensor deviation fault *)
    iCurrentState           : INT;      (* Active state machine state *)
END_VAR
VAR
    iState                  : INT := 0; (* Internal state machine tracker *)
    tStartupDelay           : TON;      (* Delay before engaging cascade control *)
    tShearTimer             : TON;      (* Timer for sustained high shear conditions *)
    
    rDO_Average             : REAL;     (* Filtered and averaged DO value *)
    rDO_Setpoint            : REAL := 30.0; (* DO Setpoint [%] *)
    rDO_Error               : REAL;     (* Control error for DO *)
    
    (* Cascade PID Variables *)
    rPropGain_DO            : REAL := 1.2;
    rIntegGain_DO           : REAL := 0.05;
    rIntegSum_DO            : REAL := 0.0;
    
    rShearStress_Est        : REAL;     (* Estimated shear stress based on RPM and impeller constants *)
    rMaxAllowedShear        : REAL := 450.0; (* Maximum allowed shear to prevent cell damage *)
    
    bInitDone               : BOOL := FALSE;
END_VAR

(* === MAIN LOGIC === *)

(* Safety and Hardware Interlocks *)
IF NOT bEmergencyStop OR NOT bAgitatorDrive_OK OR NOT bSpargerValve_OK THEN
    bSystemReady := FALSE;
    rAgitatorSpeed_Cmd := 0.0;
    rSpargerFlow_Cmd := 0.0;
    iState := 0;
    rIntegSum_DO := 0.0;
    iCurrentState := -1; (* Fault state *)
    RETURN;
END_IF;

(* DO Sensor Validation & Filtering (Redundancy Check) *)
IF ABS(rDO_Measurement_1 - rDO_Measurement_2) > 10.0 THEN
    bAlarm_SensorFault := TRUE;
    (* Fallback to the lowest reading to be conservative on DO supply *)
    IF rDO_Measurement_1 < rDO_Measurement_2 THEN
        rDO_Average := rDO_Measurement_1;
    ELSE
        rDO_Average := rDO_Measurement_2;
    END_IF;
ELSE
    bAlarm_SensorFault := FALSE;
    rDO_Average := (rDO_Measurement_1 + rDO_Measurement_2) / 2.0;
END_IF;

(* Critical Hypoxia Check *)
IF rDO_Average < 5.0 THEN
    bAlarm_LowDO := TRUE;
ELSE
    bAlarm_LowDO := FALSE;
END_IF;

(* Shear Stress Estimation (Simplified Power Number Model) *)
(* Shear ~ RPM^1.5 for this specific Ruston turbine impeller in broth *)
rShearStress_Est := EXPT(rAgitatorSpeed_Fdbk, 1.5) * 0.085;
IF rShearStress_Est > rMaxAllowedShear THEN
    tShearTimer(IN := TRUE, PT := T#10S);
    IF tShearTimer.Q THEN
        bAlarm_HighShear := TRUE;
    END_IF;
ELSE
    tShearTimer(IN := FALSE);
    bAlarm_HighShear := FALSE;
END_IF;


(* State Machine for Bioreactor DO Cascade Control *)
CASE iState OF
    0: (* IDLE / STANDBY *)
        bSystemReady := TRUE;
        rAgitatorSpeed_Cmd := 50.0; (* Minimum mixing speed *)
        rSpargerFlow_Cmd := 10.0;   (* Sweep gas flow *)
        
        IF bEnable THEN
            iState := 10;
        END_IF;

    10: (* STARTUP / EQUILIBRATION *)
        tStartupDelay(IN := TRUE, PT := T#30S);
        rAgitatorSpeed_Cmd := 100.0;
        rSpargerFlow_Cmd := 50.0;
        
        IF tStartupDelay.Q THEN
            tStartupDelay(IN := FALSE);
            iState := 20;
        END_IF;
        IF NOT bEnable THEN
            tStartupDelay(IN := FALSE);
            iState := 0;
        END_IF;

    20: (* ACTIVE CASCADE CONTROL *)
        rDO_Error := rDO_Setpoint - rDO_Average;
        
        (* Anti-windup PI Control for Base Aeration (Sparger) *)
        rIntegSum_DO := rIntegSum_DO + (rDO_Error * rIntegGain_DO);
        IF rIntegSum_DO > 500.0 THEN rIntegSum_DO := 500.0; END_IF;
        IF rIntegSum_DO < 0.0 THEN rIntegSum_DO := 0.0; END_IF;
        
        rSpargerFlow_Cmd := (rDO_Error * rPropGain_DO) + rIntegSum_DO;
        
        (* Limit Sparger Flow *)
        IF rSpargerFlow_Cmd > 1000.0 THEN rSpargerFlow_Cmd := 1000.0; END_IF;
        IF rSpargerFlow_Cmd < 50.0 THEN rSpargerFlow_Cmd := 50.0; END_IF;
        
        (* Agitator Speed Supplement (O2 Mass Transfer Boost) *)
        (* If sparger is maxed out and DO is still low, increase agitation *)
        IF rSpargerFlow_Cmd >= 950.0 AND rDO_Error > 5.0 THEN
            rAgitatorSpeed_Cmd := rAgitatorSpeed_Cmd + 1.0;
        ELSIF rDO_Error < -2.0 AND rAgitatorSpeed_Cmd > 100.0 THEN
            rAgitatorSpeed_Cmd := rAgitatorSpeed_Cmd - 1.0;
        END_IF;
        
        (* Protect cells from high shear *)
        IF bAlarm_HighShear THEN
            rAgitatorSpeed_Cmd := rAgitatorSpeed_Cmd - 10.0; (* Back off speed aggressively *)
        END_IF;
        
        (* Agitator Limits *)
        IF rAgitatorSpeed_Cmd > 800.0 THEN rAgitatorSpeed_Cmd := 800.0; END_IF;
        IF rAgitatorSpeed_Cmd < 100.0 THEN rAgitatorSpeed_Cmd := 100.0; END_IF;
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    ELSE
        (* INVALID STATE RECOVERY *)
        iState := 0;
END_CASE;

iCurrentState := iState;

END_FUNCTION_BLOCK
```"""

import os
os.makedirs("data/swarm_raw", exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print("Saved")
