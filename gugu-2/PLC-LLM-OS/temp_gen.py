import json
import uuid
import os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: High-Throughput Pharmaceutical Blister Packaging Thermoforming and Sealing**

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Pharma_BlisterPackaging\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: High-Throughput Pharmaceutical Blister Packaging Thermoforming and Sealing

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_PharmaBlisterThermoSeal
VAR_INPUT
    bEnable                 : BOOL;     (* System master enable signal *)
    bEmergencyStop          : BOOL;     (* Safety relay OK signal (Normally Closed, 1=OK) *)
    bGuardDoorsClosed       : BOOL;     (* Safety interlock for guarding doors *)
    rTempZone1_C            : REAL;     (* Thermoforming heating zone 1 temperature [°C] *)
    rTempZone2_C            : REAL;     (* Thermoforming heating zone 2 temperature [°C] *)
    rSealPressure_Bar       : REAL;     (* Sealing station pneumatic pressure [Bar] *)
    rFoilTension_N          : REAL;     (* Forming foil web tension [N] *)
    rLineSpeed_mm_s         : REAL;     (* Conveyor web speed [mm/s] *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* Thermoformer is at temperature and ready *)
    bRunning                : BOOL;     (* Machine is actively forming and sealing *)
    rHeaterControl1_Pct     : REAL;     (* Zone 1 heater control signal (0-100%) *)
    rHeaterControl2_Pct     : REAL;     (* Zone 2 heater control signal (0-100%) *)
    bWebAdvanceCmd          : BOOL;     (* Command to index the foil web *)
    bSealActuateCmd         : BOOL;     (* Command to actuate the sealing die *)
    bAlarm                  : BOOL;     (* Fault alarm output *)
    iAlarmCode              : INT;      (* Detailed alarm code for HMI *)
END_VAR
VAR
    (* Internal state variables *)
    iState                  : INT := 0;
    
    (* Filtered Inputs *)
    rFiltTempZone1          : REAL;
    rFiltTempZone2          : REAL;
    rFiltSealPressure       : REAL;
    
    (* PID Controllers *)
    pidZone1                : PID_STANDARD;
    pidZone2                : PID_STANDARD;
    
    (* Timers *)
    tIndexTimer             : TON;
    tSealTimer              : TON;
    tHeatUpTimeout          : TON;
    tWatchdog               : TON;
    
    (* Configuration / Setpoints *)
    rSetTemp1               : REAL := 145.0;
    rSetTemp2               : REAL := 150.0;
    rMinPressure            : REAL := 5.5;
    tIndexDuration          : TIME := T#200MS;
    tSealDuration           : TIME := T#400MS;
    tMaxHeatTime            : TIME := T#10M;
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety & Interlocks *)
IF NOT bEmergencyStop OR NOT bGuardDoorsClosed THEN
    bSystemReady := FALSE;
    bRunning := FALSE;
    bWebAdvanceCmd := FALSE;
    bSealActuateCmd := FALSE;
    rHeaterControl1_Pct := 0.0;
    rHeaterControl2_Pct := 0.0;
    bAlarm := TRUE;
    iAlarmCode := 1001; (* E-Stop or Guard Open *)
    iState := 999; (* Fault State *)
    RETURN;
END_IF;

(* 2. Signal Filtering (First-order low pass for noisy sensors) *)
rFiltTempZone1 := rFiltTempZone1 + 0.1 * (rTempZone1_C - rFiltTempZone1);
rFiltTempZone2 := rFiltTempZone2 + 0.1 * (rTempZone2_C - rFiltTempZone2);
rFiltSealPressure := rFiltSealPressure + 0.2 * (rSealPressure_Bar - rFiltSealPressure);

(* 3. Process PID Control for Heaters *)
pidZone1(
    bEnable := (iState > 0 AND iState < 999),
    rSetpoint := rSetTemp1,
    rProcessValue := rFiltTempZone1,
    rKp := 2.5, rTi := 120.0, rTd := 5.0,
    rOutput => rHeaterControl1_Pct
);

pidZone2(
    bEnable := (iState > 0 AND iState < 999),
    rSetpoint := rSetTemp2,
    rProcessValue := rFiltTempZone2,
    rKp := 2.2, rTi := 130.0, rTd := 4.5,
    rOutput => rHeaterControl2_Pct
);

(* 4. Main State Machine *)
CASE iState OF
    0: (* IDLE & INITIALIZATION *)
        bSystemReady := FALSE;
        bRunning := FALSE;
        bAlarm := FALSE;
        iAlarmCode := 0;
        IF bEnable THEN
            iState := 10;
            tHeatUpTimeout(IN:=FALSE);
        END_IF;

    10: (* HEATING PHASE *)
        (* Wait for both zones to reach operating temperature range +/- 2 deg *)
        tHeatUpTimeout(IN:=TRUE, PT:=tMaxHeatTime);
        IF tHeatUpTimeout.Q THEN
            bAlarm := TRUE;
            iAlarmCode := 2001; (* Heat-up timeout *)
            iState := 999;
        ELSIF (ABS(rFiltTempZone1 - rSetTemp1) < 2.0) AND (ABS(rFiltTempZone2 - rSetTemp2) < 2.0) THEN
            IF rFiltSealPressure >= rMinPressure THEN
                bSystemReady := TRUE;
                iState := 20;
            END_IF;
        END_IF;

    20: (* READY TO RUN *)
        IF NOT bEnable THEN
            iState := 0;
        ELSIF bEnable AND (rFiltSealPressure < rMinPressure) THEN
            bAlarm := TRUE;
            iAlarmCode := 3001; (* Low Air Pressure *)
            iState := 999;
        ELSIF bEnable THEN
            (* Operator pressed start while ready *)
            bRunning := TRUE;
            iState := 30;
        END_IF;

    30: (* ADVANCE WEB *)
        bWebAdvanceCmd := TRUE;
        tIndexTimer(IN:=TRUE, PT:=tIndexDuration);
        IF tIndexTimer.Q THEN
            bWebAdvanceCmd := FALSE;
            tIndexTimer(IN:=FALSE);
            iState := 40;
        END_IF;

    40: (* FORMING AND SEALING DWELL *)
        bSealActuateCmd := TRUE;
        tSealTimer(IN:=TRUE, PT:=tSealDuration);
        IF tSealTimer.Q THEN
            bSealActuateCmd := FALSE;
            tSealTimer(IN:=FALSE);
            iState := 30; (* Loop back to advance web *)
        END_IF;
        
        (* Watchdog on Pressure drop during seal *)
        IF rFiltSealPressure < (rMinPressure * 0.8) THEN
            bAlarm := TRUE;
            iAlarmCode := 3002; (* Pressure drop during seal *)
            iState := 999;
        END_IF;
        
        IF NOT bEnable THEN
            bRunning := FALSE;
            bSealActuateCmd := FALSE;
            iState := 20;
        END_IF;

    999: (* FAULT HANDLING *)
        bSystemReady := FALSE;
        bRunning := FALSE;
        bWebAdvanceCmd := FALSE;
        bSealActuateCmd := FALSE;
        rHeaterControl1_Pct := 0.0;
        rHeaterControl2_Pct := 0.0;
        IF NOT bEnable AND bEmergencyStop AND bGuardDoorsClosed THEN
            bAlarm := FALSE;
            iState := 0; (* Reset fault on disable *)
        END_IF;
        
END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
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
