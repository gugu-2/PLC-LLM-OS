import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Utility-Scale Flywheel Energy Storage (FES) Vacuum Enclosure**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 100,000 RPM carbon-fiber rotor active magnetic bearing (AMB) levitation, high-vacuum molecular drag pump cascading, and multi-megawatt stator back-EMF synchronous switching). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\nFUNCTION_BLOCK FB_FlywheelEnergyStorage\n//...\nEND_FUNCTION_BLOCK\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Utility-Scale Flywheel Energy Storage (FES) Vacuum Enclosure

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_FES_VacuumEnclosureCtrl
VAR_INPUT
    bSystemEnable       : BOOL;     (* Main activation signal for the entire FES subsystem *)
    bEmergencyStop      : BOOL;     (* Safety relay OK signal; TRUE = safe, FALSE = trip *)
    rVacuumPressure     : REAL;     (* Enclosure internal pressure in mBar (e.g. 1e-5 mBar target) *)
    rRotorSpeed         : REAL;     (* Current rotor speed in RPM (max 100,000 RPM) *)
    rAMBLevitationGap   : REAL;     (* Active Magnetic Bearing radial gap measurement in mm *)
    rStatorTemp         : REAL;     (* Stator winding temperature in deg C *)
    rVibrationRMS       : REAL;     (* Rotor vibration RMS value in mm/s *)
    rGridFreq           : REAL;     (* Grid frequency in Hz for synchronous injection *)
END_VAR
VAR_OUTPUT
    bSystemReady        : BOOL;     (* High when levitation, vacuum, and thermals are nominal *)
    rDriveTorqueRef     : REAL;     (* Torque reference to motor/generator drive in Nm *)
    bVacuumPumpStart    : BOOL;     (* Command to start molecular drag pump *)
    bAMBActive          : BOOL;     (* Active Magnetic Bearing levitation engaged *)
    bTripAlarm          : BOOL;     (* Major system fault alarm *)
    rEstimatedLosses    : REAL;     (* Calculated aerodynamic and magnetic drag loss (W) *)
END_VAR
VAR
    iState              : INT := 0; (* Internal state machine *)
    tPumpTimer          : TON;      (* Timer for vacuum pump sequence *)
    tDelay              : TON;      (* General purpose delay *)
    rFilteredPressure   : REAL := 1013.0; (* Low-pass filtered vacuum pressure *)
    rAlpha              : REAL := 0.05; (* Filter coefficient *)
    bLevitationOK       : BOOL := FALSE;
    bVacuumOK           : BOOL := FALSE;
    rMaxVibration       : REAL := 2.5; (* Trip threshold for vibration mm/s *)
    rMaxTemp            : REAL := 120.0; (* Trip threshold for stator temp deg C *)
END_VAR

(* === MAIN LOGIC === *)
(* 1. Safety Interlocks & Fault Detection *)
IF NOT bEmergencyStop OR (rVibrationRMS > rMaxVibration) OR (rStatorTemp > rMaxTemp) THEN
    bSystemReady := FALSE;
    bTripAlarm := TRUE;
    bAMBActive := FALSE; (* Drop rotor onto touchdown bearings in emergency *)
    rDriveTorqueRef := 0.0;
    bVacuumPumpStart := FALSE;
    iState := 999; (* FAULT STATE *)
    RETURN;
END_IF;

(* 2. Sensor Signal Processing (First-order IIR Filter for Vacuum) *)
rFilteredPressure := rFilteredPressure + rAlpha * (rVacuumPressure - rFilteredPressure);

(* Evaluate primary operational permissives *)
bVacuumOK := (rFilteredPressure < 0.01); (* 1e-2 mBar threshold *)
bLevitationOK := (rAMBLevitationGap > 0.4) AND (rAMBLevitationGap < 0.6); (* Nominal gap ~0.5mm *)

(* 3. Core State Machine *)
CASE iState OF
    0: (* OFF / STANDBY *)
        bSystemReady := FALSE;
        bTripAlarm := FALSE;
        bVacuumPumpStart := FALSE;
        bAMBActive := FALSE;
        rDriveTorqueRef := 0.0;
        
        IF bSystemEnable THEN
            iState := 10;
        END_IF;

    10: (* VACUUM PUMPDOWN PHASE *)
        bVacuumPumpStart := TRUE;
        tPumpTimer(IN := TRUE, PT := T#5M); (* Wait for roughing and molecular pumps *)
        
        IF bVacuumOK THEN
            tPumpTimer(IN := FALSE);
            iState := 20;
        ELSIF tPumpTimer.Q THEN
            (* Pumpdown timeout fault *)
            bTripAlarm := TRUE;
            iState := 999;
        END_IF;

    20: (* LEVITATION ENGAGEMENT *)
        bAMBActive := TRUE;
        tDelay(IN := TRUE, PT := T#10S); (* Allow AMB controllers to stabilize *)
        
        IF tDelay.Q AND bLevitationOK THEN
            tDelay(IN := FALSE);
            iState := 30;
        END_IF;

    30: (* SPIN-UP / SYNCHRONOUS READY *)
        bSystemReady := TRUE;
        
        (* Calculate dynamic loss estimation based on pressure and speed *)
        rEstimatedLosses := (rFilteredPressure * rRotorSpeed * 0.0001) + (rRotorSpeed * 0.0005);
        
        (* Example speed regulation loop (proportional control placeholder) *)
        IF rRotorSpeed < 90000.0 THEN
            rDriveTorqueRef := 500.0; (* Accelerate *)
        ELSIF rRotorSpeed >= 100000.0 THEN
            rDriveTorqueRef := 0.0; (* Coast or generate *)
        ELSE
            rDriveTorqueRef := 50.0; (* Maintain speed *)
        END_IF;
        
        IF NOT bSystemEnable THEN
            iState := 40;
        END_IF;
        
    40: (* SPIN-DOWN / SHUTDOWN *)
        bSystemReady := FALSE;
        rDriveTorqueRef := -500.0; (* Regenerative braking *)
        
        IF rRotorSpeed < 100.0 THEN
            iState := 0; (* Return to standby when safely stopped *)
        END_IF;

    999: (* FAULT HANDLING *)
        (* Latch fault until enable is removed *)
        IF NOT bSystemEnable THEN
            bTripAlarm := FALSE;
            iState := 0;
        END_IF;
END_CASE;

END_FUNCTION_BLOCK
```"""

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
