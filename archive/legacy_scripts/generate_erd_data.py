import json, uuid
import os

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial Scale Seawater Reverse Osmosis (SWRO) Energy Recovery Device (ERD)**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Isobaric pressure exchanger rotor synchronization, variable frequency drive booster pump feed-forward pressure matching, and biofouling membrane differential osmotic cleaning). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_SWRO_EnergyRecovery\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
   record = {\"messages\": [{\"role\": \"user\", \"content\": prompt}, {\"role\": \"assistant\", \"content\": code}]}
   with open(f\"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json\", \"w\", encoding=\"utf-8\") as f:
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Scale Seawater Reverse Osmosis (SWRO) Energy Recovery Device (ERD)

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_SWRO_IsobaricERD_Sync
VAR_INPUT
    bSystemEnable       : BOOL;     (* Main plant operational enable flag *)
    bEStopOK            : BOOL;     (* Emergency Stop Relay OK (TRUE = Healthy) *)
    bBrineFlowOK        : BOOL;     (* High Pressure Brine flow sensor status *)
    rFeedWaterTemp      : REAL;     (* Feed water temperature in °C for osmotic compensation *)
    rHighPressureIn     : REAL;     (* RO High Pressure Brine Inlet in Bar (Range: 50-80 Bar) *)
    rLowPressureIn      : REAL;     (* Seawater Low Pressure Inlet in Bar (Range: 1-5 Bar) *)
    rRotorSpeedMeas     : REAL;     (* PX Rotor RPM feedback (0-1500 RPM) *)
    rBoosterDischargeP  : REAL;     (* Booster Pump discharge pressure in Bar *)
END_VAR
VAR_OUTPUT
    bERDReady           : BOOL;     (* ERD operational and synchronized *)
    rBoosterVFDRef      : REAL;     (* VFD Speed Reference for Booster Pump (0.0 - 100.0 %) *)
    bSyncFault          : BOOL;     (* Rotor synchronization fault flag *)
    rMixingRatioEst     : REAL;     (* Estimated volumetric mixing ratio (%) *)
    bAlarmRotorStall    : BOOL;     (* Alarm: Rotor stall detected *)
    bAlarmOverPressure  : BOOL;     (* Alarm: Excessive differential pressure *)
END_VAR
VAR
    iState              : INT := 0; 
    tStartupDelay       : TON;
    tFaultTimer         : TON;
    rFilteredRotorRPM   : REAL := 0.0;
    rAlpha              : REAL := 0.2; (* Low pass filter coefficient *)
    rTargetRotorRPM     : REAL;
    rSpeedError         : REAL;
    rPIDIntegral        : REAL := 0.0;
    rPIDKp              : REAL := 0.85;
    rPIDKi              : REAL := 0.15;
    rPIDOut             : REAL;
    rMaxPressureLim     : REAL := 82.5; (* Safety limit Bar *)
    rDeltaP             : REAL;
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety Interlocks & E-Stop *)
IF NOT bEStopOK THEN
    bERDReady := FALSE;
    rBoosterVFDRef := 0.0;
    bAlarmRotorStall := FALSE;
    bAlarmOverPressure := FALSE;
    iState := 0;
    RETURN;
END_IF;

(* 2. Overpressure Safety Check *)
IF (rHighPressureIn > rMaxPressureLim) OR (rBoosterDischargeP > rMaxPressureLim) THEN
    bAlarmOverPressure := TRUE;
    rBoosterVFDRef := 0.0;
    iState := 99; (* Fault state *)
ELSE
    bAlarmOverPressure := FALSE;
END_IF;

(* 3. Sensor Noise Filtering - First order low-pass for Rotor RPM *)
rFilteredRotorRPM := (rAlpha * rRotorSpeedMeas) + ((1.0 - rAlpha) * rFilteredRotorRPM);

(* 4. Differential Pressure Calculation for leakage estimation *)
rDeltaP := rHighPressureIn - rLowPressureIn;

(* 5. Main ERD State Machine *)
CASE iState OF
    0: (* SYSTEM IDLE *)
        bERDReady := FALSE;
        rBoosterVFDRef := 0.0;
        bSyncFault := FALSE;
        bAlarmRotorStall := FALSE;
        rPIDIntegral := 0.0;
        
        IF bSystemEnable AND bBrineFlowOK AND NOT bAlarmOverPressure THEN
            iState := 10;
        END_IF;

    10: (* PRIMING & FLUSHING *)
        (* Start booster pump at minimum safe speed to flush rotor *)
        rBoosterVFDRef := 15.0; 
        tStartupDelay(IN := TRUE, PT := T#10S);
        
        IF tStartupDelay.Q THEN
            tStartupDelay(IN := FALSE);
            IF rFilteredRotorRPM > 50.0 THEN
                iState := 20; (* Proceed to sync *)
            ELSE
                bAlarmRotorStall := TRUE;
                iState := 99; (* Transition to fault *)
            END_IF;
        END_IF;

    20: (* ROTOR SYNCHRONIZATION AND PID CONTROL *)
        bERDReady := TRUE;
        
        (* Calculate dynamic target RPM based on HP Brine flow logic & temperature viscosity compensation *)
        rTargetRotorRPM := 800.0 + (rDeltaP * 2.5) - (rFeedWaterTemp * 1.2);
        
        IF rTargetRotorRPM > 1200.0 THEN rTargetRotorRPM := 1200.0; END_IF;
        IF rTargetRotorRPM < 400.0 THEN rTargetRotorRPM := 400.0; END_IF;
        
        (* PID execution for Booster Pump VFD speed *)
        rSpeedError := rTargetRotorRPM - rFilteredRotorRPM;
        
        (* Anti-windup integration *)
        IF (rPIDOut < 100.0 AND rSpeedError > 0.0) OR (rPIDOut > 20.0 AND rSpeedError < 0.0) THEN
            rPIDIntegral := rPIDIntegral + (rSpeedError * rPIDKi);
        END_IF;
        
        rPIDOut := (rSpeedError * rPIDKp) + rPIDIntegral;
        
        (* Output saturation limit for VFD (20% to 100%) *)
        IF rPIDOut > 100.0 THEN
            rBoosterVFDRef := 100.0;
        ELSIF rPIDOut < 20.0 THEN
            rBoosterVFDRef := 20.0;
        ELSE
            rBoosterVFDRef := rPIDOut;
        END_IF;

        (* Calculate Estimated Mixing Ratio (volumetric mixing) *)
        rMixingRatioEst := (rDeltaP / 80.0) * (rFilteredRotorRPM / 1500.0) * 100.0;
        
        (* Fault monitoring: Sync loss *)
        IF ABS(rSpeedError) > 200.0 THEN
            tFaultTimer(IN := TRUE, PT := T#5S);
            IF tFaultTimer.Q THEN
                bSyncFault := TRUE;
                iState := 99;
            END_IF;
        ELSE
            tFaultTimer(IN := FALSE);
        END_IF;
        
        IF NOT bSystemEnable THEN
            tFaultTimer(IN := FALSE);
            iState := 0;
        END_IF;
        
    99: (* FAULT HANDLING *)
        bERDReady := FALSE;
        rBoosterVFDRef := 0.0;
        tStartupDelay(IN := FALSE);
        tFaultTimer(IN := FALSE);
        
        IF NOT bSystemEnable AND NOT bAlarmOverPressure THEN
            (* Reset fault state when enable is dropped *)
            bSyncFault := FALSE;
            bAlarmRotorStall := FALSE;
            iState := 0;
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
