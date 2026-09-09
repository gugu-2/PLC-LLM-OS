import os, json, uuid

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Advanced Spacecraft Xenon Hall-Effect Thruster**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., High-voltage anode magnetic shielding mapping, xenon mass-flow proportional valving, and cathode neutralizer emission current matching). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_HallEffectThruster\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Advanced Spacecraft Xenon Hall-Effect Thruster

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_XenonHallEffectThruster
VAR_INPUT
    bSystemEnable           : BOOL;     (* Main power and system enable signal *)
    bEmergencyInterlock     : BOOL;     (* Hardware emergency shutdown signal (active high = OK) *)
    rDischargeVoltage       : REAL;     (* Measured discharge voltage (V) *)
    rDischargeCurrent       : REAL;     (* Measured discharge current (A) *)
    rXenonInletPressure     : REAL;     (* Xenon tank regulator inlet pressure (psia) *)
    rAnodeTemp              : REAL;     (* Anode temperature measurement (Deg C) *)
    rCathodeTemp            : REAL;     (* Cathode temperature measurement (Deg C) *)
    rCathodeEmissionCurr    : REAL;     (* Neutralizer cathode emission current (A) *)
END_VAR
VAR_OUTPUT
    bThrusterReady          : BOOL;     (* Thruster system initialization complete and ready to fire *)
    bThrusterFiring         : BOOL;     (* Thruster is actively firing (beam extraction active) *)
    rXenonFlowValveCmd      : REAL;     (* Command to proportional flow control valve (0-100%) *)
    rAnodePowerCmd          : REAL;     (* Commanded anode discharge power setpoint (W) *)
    rMagnetCurrentCmd       : REAL;     (* Magnetic shielding coil current command (A) *)
    bCriticalFault          : BOOL;     (* Critical fault active, thruster shutdown *)
END_VAR
VAR
    iOpState                : INT := 0; (* Internal State Machine variable *)
    tIgnitionTimer          : TON;      (* Timer for ignition sequencing *)
    tCathodeWarmupTimer     : TON;      (* Timer for cathode heater warmup phase *)
    rCalculatedMassFlow     : REAL;     (* Internally calculated mass flow rate (mg/s) *)
    rImpedance              : REAL;     (* Calculated plasma impedance (Ohms) *)
    
    (* Constants *)
    rMAX_ANODE_TEMP         : REAL := 450.0;
    rMIN_CATHODE_TEMP       : REAL := 1050.0;
    rNOMINAL_DISCHARGE_V    : REAL := 300.0;
    rFLOW_KP                : REAL := 0.25;
END_VAR

(* === MAIN LOGIC === *)
(* Safety Interlock Evaluation *)
IF NOT bEmergencyInterlock OR (rAnodeTemp > rMAX_ANODE_TEMP) THEN
    bThrusterReady := FALSE;
    bThrusterFiring := FALSE;
    bCriticalFault := TRUE;
    rXenonFlowValveCmd := 0.0;
    rAnodePowerCmd := 0.0;
    rMagnetCurrentCmd := 0.0;
    iOpState := 99; (* FAULT STATE *)
    RETURN;
END_IF;

(* Plasma Impedance Calculation (prevent div by zero) *)
IF rDischargeCurrent > 0.01 THEN
    rImpedance := rDischargeVoltage / rDischargeCurrent;
ELSE
    rImpedance := 9999.0;
END_IF;

(* Main Control State Machine *)
CASE iOpState OF
    0: (* IDLE & STANDBY *)
        bThrusterReady := FALSE;
        bThrusterFiring := FALSE;
        bCriticalFault := FALSE;
        rXenonFlowValveCmd := 0.0;
        rAnodePowerCmd := 0.0;
        rMagnetCurrentCmd := 0.0;
        
        IF bSystemEnable THEN
            iOpState := 10;
        END_IF;

    10: (* CATHODE HEATING *)
        (* Warm up the neutralizer cathode before introducing propellant *)
        tCathodeWarmupTimer(IN := TRUE, PT := T#120S);
        IF tCathodeWarmupTimer.Q AND (rCathodeTemp >= rMIN_CATHODE_TEMP) THEN
            tCathodeWarmupTimer(IN := FALSE);
            iOpState := 20;
        END_IF;

    20: (* PROPELLANT PRIMING *)
        (* Establish nominal xenon flow before applying discharge voltage *)
        rXenonFlowValveCmd := 15.0; (* 15% valve opening for prime *)
        bThrusterReady := TRUE;
        
        (* Wait for operator or higher level controller to command firing, assuming bSystemEnable remains TRUE *)
        IF rXenonInletPressure > 20.0 THEN
            iOpState := 30;
        END_IF;

    30: (* IGNITION SEQUENCE *)
        bThrusterFiring := TRUE;
        rAnodePowerCmd := rNOMINAL_DISCHARGE_V * 2.0; (* Pre-ignition power cmd *)
        rMagnetCurrentCmd := 1.5; (* Nominal magnetic shielding current *)
        
        tIgnitionTimer(IN := TRUE, PT := T#5S);
        IF tIgnitionTimer.Q THEN
            tIgnitionTimer(IN := FALSE);
            IF rDischargeCurrent > 0.5 THEN
                (* Ignition successful, plasma established *)
                iOpState := 40;
            ELSE
                (* Failed to ignite *)
                bCriticalFault := TRUE;
                iOpState := 99;
            END_IF;
        END_IF;

    40: (* NOMINAL STEADY-STATE FIRING *)
        (* Closed-loop control of mass flow to maintain target discharge current *)
        rCalculatedMassFlow := rDischargeCurrent * 0.85; (* Simplified relationship *)
        
        (* Simple Proportional Control for Xenon Valve based on discharge current matching *)
        IF rCathodeEmissionCurr < rDischargeCurrent THEN
            rXenonFlowValveCmd := rXenonFlowValveCmd + rFLOW_KP;
        ELSIF rCathodeEmissionCurr > rDischargeCurrent THEN
            rXenonFlowValveCmd := rXenonFlowValveCmd - rFLOW_KP;
        END_IF;
        
        (* Limit Valve Command *)
        IF rXenonFlowValveCmd > 100.0 THEN
            rXenonFlowValveCmd := 100.0;
        ELSIF rXenonFlowValveCmd < 0.0 THEN
            rXenonFlowValveCmd := 0.0;
        END_IF;

        IF NOT bSystemEnable THEN
            iOpState := 0;
        END_IF;

    99: (* FAULT HANDLING *)
        bThrusterFiring := FALSE;
        rXenonFlowValveCmd := 0.0;
        rAnodePowerCmd := 0.0;
        rMagnetCurrentCmd := 0.0;
        
        IF NOT bSystemEnable THEN
            (* Require system disable to reset fault *)
            bCriticalFault := FALSE;
            iOpState := 0;
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
