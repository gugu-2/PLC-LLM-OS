import os, json, uuid

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Utility-Scale Kinetic Flywheel Energy Storage (FESS) Vacuum Enclosure**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Active magnetic bearing (AMB) synchronous vibration unbalance rejection, 60,000 RPM carbon-composite rotor centrifugal strain monitoring, and high-vacuum outgassing getter-pump integration). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_FESS_FlywheelStorage\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Utility-Scale Kinetic Flywheel Energy Storage (FESS) Vacuum Enclosure

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_FESS_VacuumEnclosureControl
VAR_INPUT
    bSystemEnable           : BOOL;     (* Main utility-scale energy storage system enable *)
    bEStopInterlock         : BOOL;     (* Hardware emergency stop circuit healthy *)
    rRotorSpeed_RPM         : REAL;     (* Flywheel rotor speed in Revolutions Per Minute, nominal up to 60000 RPM *)
    rVibration_um           : REAL;     (* Maximum synchronous unbalance vibration amplitude in micrometers from AMB sensors *)
    rVacuumLevel_mbar       : REAL;     (* Enclosure vacuum level in millibar *)
    rBearingTemp_C          : REAL;     (* Active Magnetic Bearing (AMB) stator winding temperature in degrees Celsius *)
    rCoolantFlow_Lpm        : REAL;     (* Cooling loop flow rate in liters per minute *)
    bGetterPumpStatus       : BOOL;     (* High-vacuum outgassing getter-pump running and healthy feedback *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* Ready to charge/discharge energy *)
    rVacuumPumpControl_Pct  : REAL;     (* Vacuum turbomolecular pump speed command in percentage (0.0 to 100.0%) *)
    rCoolantValve_Pct       : REAL;     (* AMB cooling water proportional valve command in percentage (0.0 to 100.0%) *)
    bCriticalAlarm          : BOOL;     (* Safe state activated due to critical limit violation (e.g., strain or vacuum) *)
    bWarningAlarm           : BOOL;     (* Non-critical warning (e.g., getter-pump regeneration needed) *)
    rAMBDampingFactor       : REAL;     (* Dynamic damping factor adjustment for Active Magnetic Bearing control loop *)
END_VAR
VAR
    iStateMachine           : INT := 0; (* Internal state tracking variable *)
    tDelayTimer             : TON;      (* Transition stabilization timer *)
    tVacuumSpikeTimer       : TON;      (* Outgassing transient filter timer *)
    
    (* Filtered signals *)
    rFilteredVibration      : REAL := 0.0;
    rFilteredVacuum         : REAL := 1.0; (* Initialize to atmospheric *)
    
    (* Configurable Setpoints and Limits *)
    c_rMaxSpeed_RPM         : REAL := 60000.0;
    c_rMaxVibration_um      : REAL := 150.0;
    c_rTripVibration_um     : REAL := 250.0;
    c_rTargetVacuum_mbar    : REAL := 1.0E-4;
    c_rCriticalVacuum_mbar  : REAL := 1.0E-2;
    c_rMaxTemp_C            : REAL := 95.0;
    
    (* EWMA Filter Coefficient *)
    c_rAlphaFilter          : REAL := 0.05;
END_VAR

(* === MAIN SAFETY INTERLOCKS AND SIGNAL PROCESSING === *)
IF NOT bEStopInterlock THEN
    bSystemReady := FALSE;
    bCriticalAlarm := TRUE;
    rVacuumPumpControl_Pct := 0.0;
    rCoolantValve_Pct := 100.0; (* Fail-safe cooling active *)
    iStateMachine := 999; (* Emergency state *)
    RETURN;
END_IF;

(* Exponential Weighted Moving Average (EWMA) for noisy high-frequency sensor data *)
rFilteredVibration := (c_rAlphaFilter * rVibration_um) + ((1.0 - c_rAlphaFilter) * rFilteredVibration);
rFilteredVacuum := (c_rAlphaFilter * rVacuumLevel_mbar) + ((1.0 - c_rAlphaFilter) * rFilteredVacuum);

(* Continuous Strain and Thermal Monitoring *)
IF rBearingTemp_C > c_rMaxTemp_C OR rFilteredVibration > c_rTripVibration_um THEN
    bCriticalAlarm := TRUE;
    bSystemReady := FALSE;
    rCoolantValve_Pct := 100.0;
    rAMBDampingFactor := 1.0; (* Maximize AMB stiffness/damping for run-down *)
    iStateMachine := 999;
    RETURN;
END_IF;

(* Vacuum Loss Tolerance and Getter-Pump Integration *)
tVacuumSpikeTimer(IN := (rFilteredVacuum > c_rCriticalVacuum_mbar), PT := T#2S);
IF tVacuumSpikeTimer.Q THEN
    bCriticalAlarm := TRUE;
    bSystemReady := FALSE;
    iStateMachine := 999;
    RETURN;
END_IF;

(* === SYNCHRONOUS UNBALANCE REJECTION & AMB DAMPING === *)
(* As the carbon-composite rotor approaches critical speeds, the AMB damping factor must adapt *)
IF rRotorSpeed_RPM > 40000.0 AND rFilteredVibration > c_rMaxVibration_um THEN
    (* Increase damping when traversing critical bending modes *)
    rAMBDampingFactor := 0.85;
    bWarningAlarm := TRUE;
ELSE
    (* Nominal stiffness/damping at steady state operational envelope *)
    rAMBDampingFactor := 0.25;
    IF rFilteredVibration < (c_rMaxVibration_um * 0.8) THEN
        bWarningAlarm := FALSE;
    END_IF;
END_IF;

(* Active Cooling Regulation based on Temp *)
IF rBearingTemp_C > 70.0 THEN
    rCoolantValve_Pct := (rBearingTemp_C - 70.0) * 4.0;
    IF rCoolantValve_Pct > 100.0 THEN rCoolantValve_Pct := 100.0; END_IF;
ELSE
    rCoolantValve_Pct := 20.0; (* Minimum maintenance flow *)
END_IF;

(* === MAIN STATE MACHINE === *)
CASE iStateMachine OF
    0: (* SYSTEM OFF / IDLE *)
        bSystemReady := FALSE;
        rVacuumPumpControl_Pct := 0.0;
        IF bSystemEnable THEN
            iStateMachine := 10;
        END_IF;

    10: (* EVACUATION PHASE *)
        (* Spin up turbomolecular pumps and wait for target vacuum *)
        rVacuumPumpControl_Pct := 100.0;
        IF rFilteredVacuum <= c_rTargetVacuum_mbar AND bGetterPumpStatus THEN
            tDelayTimer(IN := TRUE, PT := T#15S);
            IF tDelayTimer.Q THEN
                tDelayTimer(IN := FALSE);
                iStateMachine := 20;
            END_IF;
        ELSE
            tDelayTimer(IN := FALSE);
        END_IF;

    20: (* READY TO CHARGE / DISCHARGE *)
        bSystemReady := TRUE;
        rVacuumPumpControl_Pct := 50.0; (* Maintain vacuum at lower energy cost *)
        
        IF NOT bSystemEnable THEN
            iStateMachine := 0;
        END_IF;
        
    999: (* EMERGENCY RUN-DOWN / LOCKOUT *)
        bSystemReady := FALSE;
        bSystemEnable := FALSE;
        (* Require manual reset by dropping E-Stop and clearing faults *)
        IF bEStopInterlock AND (rFilteredVibration < c_rMaxVibration_um) AND (rBearingTemp_C < 50.0) THEN
            bCriticalAlarm := FALSE;
            iStateMachine := 0;
        END_IF;
        
END_CASE;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}

os.makedirs("data/swarm_raw", exist_ok=True)
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
