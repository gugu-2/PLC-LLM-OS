import os, json, uuid

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Industrial Scale High-Altitude Wind Power (HAWP) Airborne Tether Winch**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 1MW synchronous generator regenerative braking traction, cross-wind flight path cyclic tether tension optimization, and slip-ring multi-core fiber-optic telemetry bridging). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_HAWP_TetherWinch\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Industrial Scale High-Altitude Wind Power (HAWP) Airborne Tether Winch

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_HAWP_TetherWinch_Controller
(*
    =========================================================================
    BLOCK NAME: FB_HAWP_TetherWinch_Controller
    DESCRIPTION:
        Advanced deterministic controller for a 1MW High-Altitude Wind Power 
        (HAWP) airborne tether winch system. Includes regenerative braking
        traction control, cyclic tension optimization for cross-wind flight 
        paths, slip-ring telemetry integration, and multi-layered safety 
        interlocks.
    =========================================================================
*)

VAR_INPUT
    bSystemEnable           : BOOL;     (* System master enable *)
    bEmergencyStop          : BOOL;     (* Hardware E-stop OK signal (True = Safe) *)
    bTelemetryLinkOk        : BOOL;     (* Multi-core fiber-optic telemetry link status *)
    rTetherTensionAct       : REAL;     (* Actual tether tension measurement [kN] *)
    rPayoutSpeedAct         : REAL;     (* Actual tether payout speed [m/s] *)
    rGeneratorSpeedAct      : REAL;     (* Actual synchronous generator speed [RPM] *)
    rFlightAlt              : REAL;     (* Kite/glider flight altitude [m] *)
    rWindSpeedEst           : REAL;     (* Estimated wind speed at altitude [m/s] *)
END_VAR

VAR_OUTPUT
    bSystemReady            : BOOL;     (* Winch controller ready for operation *)
    rTorqueCommand          : REAL;     (* Torque reference command to drive [Nm] *)
    rBrakeCommand           : REAL;     (* Mechanical brake engagement [0.0 - 100.0%] *)
    bTetherTensionFault     : BOOL;     (* Over-tension or snap fault flag *)
    bCommsFault             : BOOL;     (* Telemetry link loss flag *)
    bActiveRegen            : BOOL;     (* Indicator for active regenerative generation *)
    iOperatingMode          : INT;      (* Current operating state code *)
END_VAR

VAR
    (* Internal State and Timers *)
    iState                  : INT := 0; 
    tCycleTimer             : TON;
    tTelemetryTimeout       : TON;
    tTensionFilter          : TON;
    
    (* Filtered and Internal Variables *)
    rFilteredTension        : REAL := 0.0;
    rTensionError           : REAL := 0.0;
    rIntegralTerm           : REAL := 0.0;
    rDerivativeTerm         : REAL := 0.0;
    rPrevTensionError       : REAL := 0.0;
    rPIDOutput              : REAL := 0.0;
    
    (* Parameters (Configurable via HMI/SCADA) *)
    rKp                     : REAL := 1.25;
    rKi                     : REAL := 0.15;
    rKd                     : REAL := 0.05;
    rTensionSetpoint        : REAL := 450.0; (* Base tension [kN] *)
    rMaxTension             : REAL := 800.0; (* Structural limit [kN] *)
    rMinTension             : REAL := 50.0;  (* Slack limit [kN] *)
    rMaxTorque              : REAL := 15000.0; (* Maximum motor/gen torque [Nm] *)
END_VAR

(* === SAFETY & INTERLOCKS === *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    rTorqueCommand := 0.0;
    rBrakeCommand := 100.0; (* Full mechanical brake *)
    bActiveRegen := FALSE;
    iState := 999; (* Fault State *)
    iOperatingMode := 999;
    RETURN;
END_IF;

(* Telemetry Watchdog Filter *)
tTelemetryTimeout(IN := NOT bTelemetryLinkOk, PT := T#200MS);
IF tTelemetryTimeout.Q THEN
    bCommsFault := TRUE;
    iState := 999;
ELSE
    bCommsFault := FALSE;
END_IF;

(* Simple first-order low-pass filter for tension noise *)
rFilteredTension := rFilteredTension + 0.1 * (rTetherTensionAct - rFilteredTension);

(* Tension Limit Checks *)
IF (rFilteredTension > rMaxTension) OR (rFilteredTension < rMinTension AND iState > 10) THEN
    bTetherTensionFault := TRUE;
    iState := 999;
ELSE
    bTetherTensionFault := FALSE;
END_IF;

(* === MAIN CONTROL STATE MACHINE === *)
CASE iState OF
    0: (* INIT / STANDBY *)
        bSystemReady := TRUE;
        rTorqueCommand := 0.0;
        rBrakeCommand := 100.0;
        bActiveRegen := FALSE;
        
        IF bSystemEnable AND NOT bCommsFault AND NOT bTetherTensionFault THEN
            iState := 10;
        END_IF;

    10: (* BRAKE RELEASE & TENSIONING *)
        rBrakeCommand := 0.0; (* Release brake *)
        rTorqueCommand := rTensionSetpoint * 5.0; (* Gentle tensioning offset *)
        
        tCycleTimer(IN := TRUE, PT := T#3S);
        IF tCycleTimer.Q THEN
            tCycleTimer(IN := FALSE);
            iState := 20;
        END_IF;

    20: (* CROSS-WIND FLIGHT PATH / TRACTION MODE (REEL OUT) *)
        (* Calculate dynamic tension setpoint based on wind and altitude profile *)
        rTensionSetpoint := 450.0 + (rWindSpeedEst * 5.0) - (rFlightAlt * 0.1);
        
        (* PID Control for Tension Tracking *)
        rTensionError := rTensionSetpoint - rFilteredTension;
        rIntegralTerm := rIntegralTerm + (rTensionError * 0.01); (* Assuming 10ms cycle *)
        
        (* Anti-windup *)
        IF rIntegralTerm > rMaxTorque THEN rIntegralTerm := rMaxTorque; END_IF;
        IF rIntegralTerm < -rMaxTorque THEN rIntegralTerm := -rMaxTorque; END_IF;
        
        rDerivativeTerm := (rTensionError - rPrevTensionError) / 0.01;
        rPIDOutput := (rKp * rTensionError) + (rKi * rIntegralTerm) + (rKd * rDerivativeTerm);
        rPrevTensionError := rTensionError;
        
        (* Map PID output to torque (regen load) *)
        rTorqueCommand := rPIDOutput;
        
        (* Clamp Torque *)
        IF rTorqueCommand > rMaxTorque THEN rTorqueCommand := rMaxTorque; END_IF;
        IF rTorqueCommand < -rMaxTorque THEN rTorqueCommand := -rMaxTorque; END_IF;
        
        (* If tether is paying out fast, we are regenerating power *)
        bActiveRegen := (rPayoutSpeedAct > 2.0) AND (rTorqueCommand > 0.0);
        
        IF NOT bSystemEnable THEN
            iState := 0;
        END_IF;

    999: (* FAULT HANDLING *)
        bSystemReady := FALSE;
        rTorqueCommand := 0.0;
        rBrakeCommand := 100.0; (* Slam brake *)
        bActiveRegen := FALSE;
        
        IF NOT bTetherTensionFault AND NOT bCommsFault AND NOT bEmergencyStop THEN
            IF bSystemEnable THEN
                iState := 0; (* Reset only when safe and enabled again *)
            END_IF;
        END_IF;

END_CASE;

iOperatingMode := iState;

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
