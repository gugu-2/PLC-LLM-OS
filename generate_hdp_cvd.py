import os, json, uuid

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Advanced Semiconductor High-Density Plasma Chemical Vapor Deposition (HDP-CVD)**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Simultaneous deposition and sputtering gap-fill optimization, dual-frequency RF bias power matching, and helium electrostatic chuck (ESC) backside cooling). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_HDP_CVD_Reactor\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Advanced Semiconductor High-Density Plasma Chemical Vapor Deposition (HDP-CVD)

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_HDP_CVD_GapFillController
VAR_INPUT
    (* Required: at least 4-8 physical inputs with types and comments *)
    bEnable               : BOOL;   (* System enable signal for HDP-CVD process *)
    bEmergencyStop        : BOOL;   (* Safety relay OK signal (Active HIGH) *)
    rLF_ForwardPower      : REAL;   (* Low Frequency (Bias) RF Forward Power Feedback (W) *)
    rHF_ForwardPower      : REAL;   (* High Frequency (Source) RF Forward Power Feedback (W) *)
    rChamberPressure      : REAL;   (* Chamber pressure measurement (mTorr) *)
    rSiH4_Flow            : REAL;   (* Silane gas flow mass flow controller feedback (sccm) *)
    rO2_Flow              : REAL;   (* Oxygen gas flow mass flow controller feedback (sccm) *)
    rAr_Flow              : REAL;   (* Argon gas flow for sputtering (sccm) *)
    rESCTemperature       : REAL;   (* Electrostatic Chuck (ESC) Temperature (deg C) *)
    rHeBacksidePressure   : REAL;   (* Helium backside cooling pressure (Torr) *)
END_VAR
VAR_OUTPUT
    (* Required: at least 3-6 outputs with types and comments *)
    bSystemReady          : BOOL;   (* System ready status for SECS/GEM host *)
    rLF_PowerSetpoint     : REAL;   (* Control signal to LF Bias RF Generator (W) *)
    rHF_PowerSetpoint     : REAL;   (* Control signal to HF Source RF Generator (W) *)
    rHeValveControl       : REAL;   (* Helium backside cooling valve position (%) *)
    bAlarm                : BOOL;   (* Fault alarm output *)
    iProcessState         : INT;    (* Internal state broadcast *)
END_VAR
VAR
    (* Internal state variables and PID elements *)
    iState                : INT := 0;
    tStepTimer            : TON;
    rDepSputterRatio      : REAL;
    rTargetRatio          : REAL := 2.75; (* Ideal Deposition-to-Sputter ratio for extreme gap fill *)
    rPlasmaDensity        : REAL;
    rTempError            : REAL;
    rHeKp                 : REAL := 2.5;
    rHeKi                 : REAL := 0.15;
    rHeIntegral           : REAL := 0.0;
    bPlasmaStruck         : BOOL := FALSE;
    rTempSetpoint         : REAL := 65.0; (* 65 C nominal for ESC processing *)
    iFaultCode            : DINT := 0;
END_VAR

(* === MAIN LOGIC === *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bAlarm := TRUE;
    iProcessState := 99;
    iFaultCode := 16#FFFF_FFFF;
    rLF_PowerSetpoint := 0.0;
    rHF_PowerSetpoint := 0.0;
    rHeValveControl := 100.0; (* Full cooling valve open on emergency abort *)
    RETURN;
END_IF;

(* Helium Backside Cooling Closed-Loop Control (ESC Temp Management) *)
rTempError := rESCTemperature - rTempSetpoint;
IF bEnable THEN
    rHeIntegral := rHeIntegral + (rTempError * 0.1); (* 100ms deterministic cycle time assumed *)
    rHeValveControl := (rTempError * rHeKp) + (rHeIntegral * rHeKi);
    
    (* Anti-windup and clamping bounds *)
    IF rHeValveControl > 100.0 THEN 
        rHeValveControl := 100.0; 
        rHeIntegral := rHeIntegral - (rTempError * 0.1); 
    END_IF;
    IF rHeValveControl < 0.0 THEN 
        rHeValveControl := 0.0; 
        rHeIntegral := rHeIntegral - (rTempError * 0.1); 
    END_IF;
ELSE
    rHeValveControl := 0.0;
    rHeIntegral := 0.0;
END_IF;

CASE iState OF
    0: (* IDLE *)
        bSystemReady := TRUE;
        bAlarm := FALSE;
        rLF_PowerSetpoint := 0.0;
        rHF_PowerSetpoint := 0.0;
        bPlasmaStruck := FALSE;
        IF bEnable THEN
            bSystemReady := FALSE;
            iState := 10;
        END_IF;

    10: (* GAS STABILIZATION *)
        tStepTimer(IN := TRUE, PT := T#5S);
        IF (rSiH4_Flow > 45.0) AND (rO2_Flow > 90.0) AND (rAr_Flow > 120.0) AND (rChamberPressure < 15.0) THEN
            IF tStepTimer.Q THEN
                tStepTimer(IN := FALSE);
                iState := 20;
            END_IF;
        END_IF;

    20: (* HIGH-FREQUENCY SOURCE PLASMA STRIKE *)
        rHF_PowerSetpoint := 3000.0; (* Strike with 3kW Source Power *)
        tStepTimer(IN := TRUE, PT := T#2S);
        IF rHF_ForwardPower > 2800.0 THEN
            bPlasmaStruck := TRUE;
            tStepTimer(IN := FALSE);
            iState := 30;
        ELSIF tStepTimer.Q THEN
            (* Failed to strike Source plasma within timeout *)
            bAlarm := TRUE;
            iFaultCode := 16#A001;
            iState := 99;
        END_IF;

    30: (* LOW-FREQUENCY BIAS STRIKE & GAP FILL MATCHING *)
        rLF_PowerSetpoint := 1500.0; (* 1.5kW Bias for sputtering aspect of HDP-CVD *)
        tStepTimer(IN := TRUE, PT := T#60S); (* Process deposition time *)
        
        (* Calculate Deposition-to-Sputter Ratio empirically using forward powers and mass flows *)
        rPlasmaDensity := (rHF_ForwardPower * 0.8) + (rLF_ForwardPower * 0.2);
        
        IF rLF_ForwardPower > 100.0 THEN
            rDepSputterRatio := (rSiH4_Flow * rHF_ForwardPower) / (rAr_Flow * rLF_ForwardPower);
        ELSE
            rDepSputterRatio := 999.0;
        END_IF;

        (* Adaptive matching constraint loop for advanced gap fill *)
        IF rDepSputterRatio > (rTargetRatio + 0.1) THEN
            rLF_PowerSetpoint := rLF_PowerSetpoint + 10.0; (* Increase sputtering yield *)
        ELSIF rDepSputterRatio < (rTargetRatio - 0.1) THEN
            rLF_PowerSetpoint := rLF_PowerSetpoint - 10.0; (* Decrease sputtering yield *)
        END_IF;

        IF tStepTimer.Q THEN
            tStepTimer(IN := FALSE);
            iState := 40;
        END_IF;

    40: (* RF RAMP DOWN *)
        (* Soft RF turn-off to prevent particle generation or micro-arcing *)
        rHF_PowerSetpoint := rHF_PowerSetpoint - 500.0;
        rLF_PowerSetpoint := rLF_PowerSetpoint - 250.0;
        IF rHF_PowerSetpoint <= 0.0 AND rLF_PowerSetpoint <= 0.0 THEN
            rHF_PowerSetpoint := 0.0;
            rLF_PowerSetpoint := 0.0;
            bPlasmaStruck := FALSE;
            iState := 50;
        END_IF;
        
    50: (* PROCESS COMPLETE *)
        bSystemReady := TRUE;
        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    99: (* FAULT HANDLING *)
        rHF_PowerSetpoint := 0.0;
        rLF_PowerSetpoint := 0.0;
        bAlarm := TRUE;
        IF NOT bEnable THEN
            iState := 0;
            iFaultCode := 0;
        END_IF;
        
END_CASE;

iProcessState := iState;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump({"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}, f, ensure_ascii=False)
print(f"Saved to {filename}")
