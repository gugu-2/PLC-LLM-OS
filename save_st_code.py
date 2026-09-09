import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Utility-Scale Solid-State Transformer (SST) Grid Interface**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Medium-voltage AC to low-voltage DC cascaded H-bridge switching, dual active bridge (DAB) zero-voltage-switching (ZVS) phase shift modulation, and harmonic distortion active filtering). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_SST_GridInterface\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Utility-Scale Solid-State Transformer (SST) Grid Interface

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_SST_GridInterface
VAR_INPUT
    bEnable                 : BOOL;     (* System master enable signal *)
    bEmergencyStop          : BOOL;     (* Hardware safety interlock (Active High = OK) *)
    rGridVoltageMV          : REAL;     (* Medium voltage AC grid measurement [kV] *)
    rGridFreq               : REAL;     (* Grid frequency measurement [Hz] *)
    rDCLinkVoltageRef       : REAL;     (* DC link voltage reference [V] *)
    rActivePowerSetpt       : REAL;     (* Desired active power injection [kW] *)
    rReactivePowerSetpt     : REAL;     (* Desired reactive power injection [kVAR] *)
    rTempDAB                : REAL;     (* Dual active bridge heatsink temp [deg C] *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* SST converter ready for grid connection *)
    bGridConnected          : BOOL;     (* Main contactor closed, switching active *)
    rModulationIndexMV      : REAL;     (* Modulation index for cascaded H-bridge *)
    rPhaseShiftDAB          : REAL;     (* Phase shift angle for DAB ZVS [rad] *)
    rDCLinkVoltageAct       : REAL;     (* Measured internal DC link voltage [V] *)
    bThermalWarning         : BOOL;     (* DAB temperature approaching limit *)
    bAlarm                  : BOOL;     (* Critical fault active, system tripped *)
    iFaultCode              : INT;      (* Diagnostics: 0=OK, 1=E-STOP, 2=Grid, 3=Thermal *)
END_VAR
VAR
    iState                  : INT := 0; (* State machine step *)
    tPrechargeTimer         : TON;      (* Timer for DC link precharge *)
    tGridSyncTimer          : TON;      (* Timer for grid synchronization stabilization *)
    rVoltageError           : REAL;
    rIntegralSum            : REAL;
    Kp_DC                   : REAL := 1.25;
    Ki_DC                   : REAL := 0.05;
    rMaxPhaseShift          : REAL := 1.5708; (* Pi/2 radians *)
END_VAR

(* === SAFETY & INTERLOCKS === *)
IF NOT bEmergencyStop THEN
    bSystemReady       := FALSE;
    bGridConnected     := FALSE;
    rModulationIndexMV := 0.0;
    rPhaseShiftDAB     := 0.0;
    bAlarm             := TRUE;
    iFaultCode         := 1;
    iState             := 0;
    RETURN;
END_IF;

(* Thermal monitoring *)
IF rTempDAB > 85.0 THEN
    bThermalWarning := TRUE;
    IF rTempDAB > 95.0 THEN
        bAlarm := TRUE;
        iFaultCode := 3;
        iState := 0;
        RETURN;
    END_IF;
ELSE
    bThermalWarning := FALSE;
END_IF;

(* === MAIN STATE MACHINE === *)
CASE iState OF
    0: (* OFF / RESET *)
        bSystemReady       := FALSE;
        bGridConnected     := FALSE;
        rModulationIndexMV := 0.0;
        rPhaseShiftDAB     := 0.0;
        IF bEnable AND NOT bAlarm THEN
            (* Check grid conditions before proceeding *)
            IF (rGridVoltageMV > 10.8 AND rGridVoltageMV < 13.2) AND (rGridFreq > 59.5 AND rGridFreq < 60.5) THEN
                iState := 10;
            ELSE
                iFaultCode := 2; (* Grid out of bounds *)
            END_IF;
        END_IF;

    10: (* PRECHARGE DC LINK *)
        (* Simulate precharge action - ramping voltage slowly *)
        tPrechargeTimer(IN := TRUE, PT := T#3S);
        IF tPrechargeTimer.Q THEN
            tPrechargeTimer(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* STANDBY / SYNCHRONIZATION *)
        bSystemReady := TRUE;
        (* Grid PLL sync delay simulation *)
        tGridSyncTimer(IN := TRUE, PT := T#2S);
        IF tGridSyncTimer.Q AND bEnable THEN
            tGridSyncTimer(IN := FALSE);
            iState := 30;
        END_IF;

    30: (* ACTIVE MODULATION & POWER TRANSFER *)
        bGridConnected := TRUE;
        
        (* Cascaded H-Bridge Modulation Control *)
        rModulationIndexMV := 0.85 + (rActivePowerSetpt * 0.0001);
        IF rModulationIndexMV > 1.0 THEN
            rModulationIndexMV := 1.0;
        END_IF;
        
        (* DAB Zero-Voltage-Switching (ZVS) Phase Shift Control *)
        (* Simple PI controller for DC link voltage via phase shift *)
        rVoltageError := rDCLinkVoltageRef - rDCLinkVoltageAct;
        rIntegralSum := rIntegralSum + (rVoltageError * Ki_DC);
        
        (* Anti-windup *)
        IF rIntegralSum > rMaxPhaseShift THEN rIntegralSum := rMaxPhaseShift; END_IF;
        IF rIntegralSum < -rMaxPhaseShift THEN rIntegralSum := -rMaxPhaseShift; END_IF;
        
        rPhaseShiftDAB := (rVoltageError * Kp_DC) + rIntegralSum;
        IF rPhaseShiftDAB > rMaxPhaseShift THEN rPhaseShiftDAB := rMaxPhaseShift; END_IF;
        IF rPhaseShiftDAB < -rMaxPhaseShift THEN rPhaseShiftDAB := -rMaxPhaseShift; END_IF;

        IF NOT bEnable THEN
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

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
