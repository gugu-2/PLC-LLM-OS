import os, json, uuid

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Advanced Spacecraft Star Tracker Optical Baffle Assembly**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Stray light rejection piezoelectric thermal compensation, multi-spectral CCD thermo-electric cooling (TEC) cascade, and quaternion attitude extrapolation filter). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_StarTrackerOpticalBaffle\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Advanced Spacecraft Star Tracker Optical Baffle Assembly

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_StarTrackerOpticalBaffle
VAR_INPUT
    (* Input Signals for Spacecraft Star Tracker Optical Assembly *)
    bEnable                 : BOOL;     (* System Enable command for star tracker assembly *)
    bEmergencyStop          : BOOL;     (* Hardware safety interlock and Emergency Stop *)
    rCCDTemperature         : REAL;     (* Measured CCD focal plane temperature (DegC) *)
    rBafflePiezoVoltFeedback: REAL;     (* Feedback voltage from stray-light piezo actuators (V) *)
    rAmbientThermalFlux     : REAL;     (* External estimated solar thermal flux (W/m2) *)
    rQuaternionW            : REAL;     (* Extrapolated attitude quaternion scalar component *)
END_VAR
VAR_OUTPUT
    (* Output Signals *)
    bSystemReady            : BOOL;     (* Optical baffle tracking system operational readiness *)
    bBaffleFaultAlarm       : BOOL;     (* Fault detected in thermal or mechanical subsystem *)
    rTECPowerOutput         : REAL;     (* Commanded TEC cascade cooling power output (W) *)
    rPiezoControlSignal     : REAL;     (* Commanded stray light compensation piezo signal (V) *)
    rFilteredAttitudeW      : REAL;     (* Noise-filtered quaternion component output for ACS *)
END_VAR
VAR
    (* Internal State and Timers *)
    iMainState              : INT := 0; (* Main control state machine integer *)
    tStartupDelay           : TON;      (* System stabilization delay timer *)
    tFaultTimer             : TON;      (* Over-temperature fault delay timer *)
    
    (* Filter and PI Controller Variables *)
    rTempFilterAcc          : REAL := 0.0;
    rPiezoErrIntegral       : REAL := 0.0;
    rPiezoError             : REAL := 0.0;
    
    (* Control Constants *)
    rTargetCCDThermal       : REAL := -45.0; (* Ideal CCD operating temp DegC *)
    rMaxCCDThermal          : REAL := -20.0; (* Max allowable CCD temp before fault *)
    rPiezoProportionalGain  : REAL := 0.15;
    rPiezoIntegralGain      : REAL := 0.005;
    rTECProportionalGain    : REAL := 2.5;
END_VAR

(* === MAIN LOGIC === *)
IF NOT bEmergencyStop THEN
    (* Immediate safe-state execution on interlock break *)
    bSystemReady := FALSE;
    bBaffleFaultAlarm := TRUE;
    rTECPowerOutput := 0.0;
    rPiezoControlSignal := 0.0;
    rFilteredAttitudeW := 0.0;
    iMainState := 99; (* Transition to fault state *)
    RETURN;
END_IF;

(* Multi-stage low-pass filtering for incoming sensor noise *)
rTempFilterAcc := (rTempFilterAcc * 0.9) + (rCCDTemperature * 0.1);

CASE iMainState OF
    0: (* IDLE AND INITIALIZATION *)
        bSystemReady := FALSE;
        bBaffleFaultAlarm := FALSE;
        rTECPowerOutput := 0.0;
        rPiezoControlSignal := 0.0;
        IF bEnable THEN
            iMainState := 10;
        END_IF;

    10: (* WARMUP AND STABILIZATION *)
        (* Engage TEC cascade at safe ramp rate *)
        tStartupDelay(IN := TRUE, PT := T#15S);
        rTECPowerOutput := (rTempFilterAcc - rTargetCCDThermal) * (rTECProportionalGain * 0.5);
        
        IF tStartupDelay.Q THEN
            IF rTempFilterAcc < rMaxCCDThermal THEN
                tStartupDelay(IN := FALSE);
                iMainState := 20;
            END_IF;
        END_IF;
        IF NOT bEnable THEN
            tStartupDelay(IN := FALSE);
            iMainState := 0;
        END_IF;

    20: (* ACTIVE TRACKING AND COMPENSATION *)
        bSystemReady := TRUE;
        
        (* Multi-spectral CCD TEC Cascade Control - Aggressive Cooling *)
        rTECPowerOutput := (rTempFilterAcc - rTargetCCDThermal) * rTECProportionalGain;
        
        (* Piezoelectric Stray Light Compensation with PI controller *)
        rPiezoError := rAmbientThermalFlux - rBafflePiezoVoltFeedback;
        rPiezoErrIntegral := rPiezoErrIntegral + (rPiezoError * rPiezoIntegralGain);
        rPiezoControlSignal := (rPiezoError * rPiezoProportionalGain) + rPiezoErrIntegral;
        
        (* Quaternion simple moving average/passthrough *)
        rFilteredAttitudeW := (rFilteredAttitudeW * 0.95) + (rQuaternionW * 0.05);

        (* Fault Detection: Over-temperature *)
        tFaultTimer(IN := (rTempFilterAcc > rMaxCCDThermal), PT := T#2S);
        IF tFaultTimer.Q THEN
            tFaultTimer(IN := FALSE);
            iMainState := 99;
        END_IF;
        
        IF NOT bEnable THEN
            iMainState := 0;
        END_IF;

    99: (* FAULT HANDLING *)
        bSystemReady := FALSE;
        bBaffleFaultAlarm := TRUE;
        rTECPowerOutput := 0.0;
        (* Maintain piezo position to prevent shock *)
        
        (* Reset from fault if cooled down and user resets enable *)
        IF NOT bEnable AND (rTempFilterAcc < rTargetCCDThermal) THEN
            bBaffleFaultAlarm := FALSE;
            iMainState := 0;
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
