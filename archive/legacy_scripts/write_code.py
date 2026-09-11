import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Semiconductor Advanced Packaging High-Bandwidth Memory (HBM) Thermocompression Bonding**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Micron-level die alignment vision servoing, pulsed localized laser reflow heating profile, and force-feedback vacuum pick-and-place tracking). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_HBM_Thermocompression\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Semiconductor Advanced Packaging High-Bandwidth Memory (HBM) Thermocompression Bonding

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_HBM_ThermoCompression_Bonding
VAR_INPUT
    (* Required: at least 4 physical inputs with types and comments *)
    bEnable             : BOOL;     (* System master enable for TC bonding sequence *)
    bEmergencyStop      : BOOL;     (* Safety relay OK / E-Stop signal. FALSE = E-STOP *)
    rVacuumLevel_mbar   : REAL;     (* Vacuum level of the pick-and-place nozzle in mbar *)
    rHeaterTemp_C       : REAL;     (* Feedback from the pulsed localized laser heater in deg C *)
    rBondForce_N        : REAL;     (* Load cell feedback for active bond force in Newtons *)
    rDieAlignX_um       : REAL;     (* Vision system X-axis die alignment error in microns *)
    rDieAlignY_um       : REAL;     (* Vision system Y-axis die alignment error in microns *)
    bVisionLock         : BOOL;     (* True when vision system confirms sub-micron alignment lock *)
END_VAR
VAR_OUTPUT
    (* Required: at least 3 outputs with types and comments *)
    bSystemReady        : BOOL;     (* System ready status, capable of receiving a new die *)
    bBondingActive      : BOOL;     (* High while the thermocompression cycle is executing *)
    rZAxisTarget_um     : REAL;     (* Commanded Z-axis position in microns for the bond head *)
    rHeaterCmd_C        : REAL;     (* Setpoint for the localized laser heater in deg C *)
    bVacuumEnable       : BOOL;     (* Command to enable/disable vacuum on the nozzle *)
    bAlarm              : BOOL;     (* Fault alarm output for SCADA / HMI *)
    iErrorCode          : INT;      (* Detailed integer error code for diagnostics *)
END_VAR
VAR
    (* Internal state variables *)
    iState              : INT := 0; (* Main sequence step *)
    tHeatingTimer       : TON;      (* Timer for the reflow heating pulse *)
    tCoolingTimer       : TON;      (* Timer for the post-bond cooling phase *)
    rForceIntegral      : REAL;     (* Integral term for force feedback PI controller *)
    rForceError         : REAL;     (* Force error computation *)
    rTargetTemp         : REAL := 285.0;  (* Reflow temperature setpoint for HBM microbumps *)
    rTargetForce        : REAL := 50.0;   (* Target bond force setpoint *)
    rVacuumThreshold    : REAL := -800.0; (* Minimum mbar threshold for safe die pickup *)
    rMaxAlignError      : REAL := 0.5;    (* Maximum allowed alignment error in microns *)
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety Interlocks & Critical Fault Checking *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bBondingActive := FALSE;
    rZAxisTarget_um := 0.0;      (* Retract safely if possible via mechanical default *)
    rHeaterCmd_C := 0.0;         (* Instantly cut power to heater *)
    bVacuumEnable := FALSE;      (* Vent vacuum *)
    bAlarm := TRUE;
    iErrorCode := 9999;          (* Critical Safety Fault Code *)
    iState := 99;
    RETURN;
END_IF;

(* 2. Continuous Vacuum Monitoring (Only check in active states) *)
IF bVacuumEnable AND (rVacuumLevel_mbar > rVacuumThreshold) AND (iState > 0) AND (iState < 70) THEN
    bAlarm := TRUE;
    iErrorCode := 1001;          (* Vacuum loss during critical operation *)
    iState := 99;
END_IF;

(* 3. Main Thermocompression Bonding Sequence *)
CASE iState OF
    0: (* IDLE - Await Master Enable *)
        bSystemReady := TRUE;
        bBondingActive := FALSE;
        bAlarm := FALSE;
        iErrorCode := 0;
        bVacuumEnable := TRUE; (* Pre-engage vacuum to secure die before cycle *)
        rZAxisTarget_um := 0.0;
        rHeaterCmd_C := 0.0;
        IF bEnable THEN
            bSystemReady := FALSE;
            bBondingActive := TRUE;
            iState := 10;
        END_IF;

    10: (* INIT_ALIGNMENT - Wait for pre-bond vacuum verification *)
        IF rVacuumLevel_mbar <= rVacuumThreshold THEN
            iState := 20;
        ELSE
            iErrorCode := 1002; (* Failed to achieve required pre-bond vacuum *)
        END_IF;

    20: (* VISION_SERVOING - Strict sub-micron die alignment *)
        IF bVisionLock AND (ABS(rDieAlignX_um) < rMaxAlignError) AND (ABS(rDieAlignY_um) < rMaxAlignError) THEN
            (* Sub-micron alignment locked, initiate safe Z-axis approach *)
            rZAxisTarget_um := -500.0; (* Fast move to approach height *)
            iState := 30;
        END_IF;

    30: (* Z_AXIS_APPROACH - Soft touchdown and active force control initiation *)
        IF rBondForce_N > 2.0 THEN
            (* Physical touchdown detected via load cell, switch to closed-loop force control *)
            rForceIntegral := 0.0;
            iState := 40;
        ELSE
            (* Incremental step-wise approach until contact *)
            rZAxisTarget_um := rZAxisTarget_um - 0.5;
        END_IF;

    40: (* FORCE_CONTROL & PULSE_HEATING - PI Control for bonding force and laser reflow profile *)
        (* Closed-loop PI force calculation *)
        rForceError := rTargetForce - rBondForce_N;
        rForceIntegral := rForceIntegral + (rForceError * 0.01);
        rZAxisTarget_um := rZAxisTarget_um - (rForceError * 0.05 + rForceIntegral * 0.001);

        (* Command localized laser reflow heater *)
        rHeaterCmd_C := rTargetTemp;

        (* Start heating pulse timer once within 2 degrees of target *)
        IF rHeaterTemp_C >= (rTargetTemp - 2.0) THEN
            tHeatingTimer(IN := TRUE, PT := T#2S); (* 2-second reflow dwell pulse *)
            IF tHeatingTimer.Q THEN
                tHeatingTimer(IN := FALSE);
                rHeaterCmd_C := 0.0; (* Extinguish heater pulse *)
                iState := 50;
            END_IF;
        END_IF;

    50: (* COOLING - Maintain compressive force while solder microbumps solidify *)
        (* Maintain active force control *)
        rForceError := rTargetForce - rBondForce_N;
        rZAxisTarget_um := rZAxisTarget_um - (rForceError * 0.05);

        (* Wait for temperature to drop below safe solidification threshold (e.g., 150 C) *)
        IF rHeaterTemp_C < 150.0 THEN
            tCoolingTimer(IN := TRUE, PT := T#1S);
            IF tCoolingTimer.Q THEN
                tCoolingTimer(IN := FALSE);
                bVacuumEnable := FALSE; (* Release die from nozzle *)
                iState := 60;
            END_IF;
        END_IF;

    60: (* RETRACT - Return Z-axis to safe stand-by clearance height *)
        rZAxisTarget_um := 0.0;
        IF NOT bEnable THEN
            iState := 0;
        END_IF;

    99: (* FAULT - System Error Handling State *)
        bSystemReady := FALSE;
        bBondingActive := FALSE;
        rHeaterCmd_C := 0.0;
        rZAxisTarget_um := 0.0; (* Retract safely *)
        (* Await fault reset by toggling Enable *)
        IF NOT bEnable AND NOT bAlarm THEN
            iState := 0; (* Reset sequence state to idle *)
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
