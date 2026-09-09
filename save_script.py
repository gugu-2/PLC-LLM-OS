import os, json, uuid
os.makedirs("data/swarm_raw", exist_ok=True)
prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Advanced Spacecraft Xenon Gridded Ion Thruster**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., High-voltage (3000V) screen grid arcing mitigation, hollow cathode neutralizer plume thermal steering, and propellant flow fraction cascade). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_IonThrusterControl\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Advanced Spacecraft Xenon Gridded Ion Thruster

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_IonThruster_AdvancedControl
VAR_INPUT
    bEnable                 : BOOL;     (* Master enable signal for the thruster *)
    bEmergencyStop          : BOOL;     (* Hardware interlock safety OK signal *)
    rScreenGridVoltage      : REAL;     (* Measured screen grid voltage [V] *)
    rScreenGridCurrent      : REAL;     (* Measured screen grid current [mA] *)
    rAccelGridVoltage       : REAL;     (* Measured accelerator grid voltage [V] *)
    rNeutralizerTemp        : REAL;     (* Hollow cathode neutralizer tip temperature [C] *)
    rXenonFlowRate          : REAL;     (* Xenon mass flow rate measurement [mg/s] *)
    bArcingDetected         : BOOL;     (* Fast hardware detection of grid arcing *)
END_VAR
VAR_OUTPUT
    bSystemReady            : BOOL;     (* Thruster control subsystem ready for plasma ignition *)
    rScreenGridVoltageSp    : REAL;     (* Setpoint for the screen grid high voltage power supply [V] *)
    rAccelGridVoltageSp     : REAL;     (* Setpoint for the accelerator grid high voltage power supply [V] *)
    rXenonFlowValvePos      : REAL;     (* Commanded position for the Xenon proportional flow valve [%] *)
    rNeutralizerHeaterPwr   : REAL;     (* Commanded power for the hollow cathode heater [%] *)
    bThrusterFault          : BOOL;     (* Critical fault latch indicating mission safety abort *)
END_VAR
VAR
    iState                  : INT := 0; (* Main state machine variable *)
    tArcRecoveryTimer       : TON;      (* Timer for arcing recovery cool-down *)
    tWarmupTimer            : TON;      (* Timer for neutralizer warmup *)
    rInternalPID_Kp         : REAL := 0.25;
    rInternalPID_Ki         : REAL := 0.05;
    rInternalPID_Error      : REAL := 0.0;
    rInternalPID_Int        : REAL := 0.0;
    iArcStrikeCounter       : INT := 0;
END_VAR

(* === MAIN LOGIC === *)
(* Immediate safety interlock check *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bThrusterFault := TRUE;
    rScreenGridVoltageSp := 0.0;
    rAccelGridVoltageSp := 0.0;
    rXenonFlowValvePos := 0.0;
    rNeutralizerHeaterPwr := 0.0;
    RETURN;
END_IF;

(* Rapid hardware arcing response - overriding state machine if severe *)
IF bArcingDetected THEN
    iArcStrikeCounter := iArcStrikeCounter + 1;
    IF iArcStrikeCounter > 5 THEN
        (* Catastrophic grid short detected *)
        bThrusterFault := TRUE;
        iState := 999; (* Fault state *)
    ELSE
        (* Normal transient arc, drop voltage to extinguish *)
        iState := 50; (* Arc recovery state *)
    END_IF;
END_IF;

CASE iState OF
    0: (* IDLE *)
        bSystemReady := FALSE;
        rScreenGridVoltageSp := 0.0;
        rAccelGridVoltageSp := 0.0;
        rXenonFlowValvePos := 0.0;
        rNeutralizerHeaterPwr := 0.0;
        
        IF bEnable THEN
            iState := 10;
        END_IF;

    10: (* NEUTRALIZER WARMUP *)
        (* Slowly ramp heater power to prevent thermal shock *)
        rNeutralizerHeaterPwr := 15.0; 
        tWarmupTimer(IN := TRUE, PT := T#300S);
        
        IF tWarmupTimer.Q AND (rNeutralizerTemp > 1050.0) THEN
            tWarmupTimer(IN := FALSE);
            iState := 20;
        END_IF;
        
    20: (* PROPELLANT FLOW ESTABLISHMENT *)
        (* Establish minimal Xenon flow for cathode ignition *)
        rXenonFlowValvePos := 5.0; 
        IF rXenonFlowRate > 1.2 THEN
            iState := 30;
        END_IF;
        
    30: (* GRID VOLTAGE RAMP (IGNITION) *)
        rAccelGridVoltageSp := -300.0; 
        rScreenGridVoltageSp := rScreenGridVoltageSp + 10.0; (* Ramp up by 10V/scan *)
        
        IF rScreenGridVoltageSp >= 3000.0 THEN
            rScreenGridVoltageSp := 3000.0;
            bSystemReady := TRUE;
            iState := 40;
        END_IF;
        
    40: (* NOMINAL THRUST OPERATION *)
        (* Implement cascade PID for precise flow control based on beam current *)
        rInternalPID_Error := 2000.0 - rScreenGridCurrent; (* Target 2A beam *)
        rInternalPID_Int := rInternalPID_Int + (rInternalPID_Error * 0.1);
        
        (* Anti-windup limits *)
        IF rInternalPID_Int > 50.0 THEN rInternalPID_Int := 50.0; END_IF;
        IF rInternalPID_Int < -50.0 THEN rInternalPID_Int := -50.0; END_IF;
        
        rXenonFlowValvePos := 20.0 + (rInternalPID_Kp * rInternalPID_Error) + (rInternalPID_Ki * rInternalPID_Int);
        
        IF NOT bEnable THEN
            iState := 0;
        END_IF;
        
    50: (* ARC RECOVERY MODE *)
        rScreenGridVoltageSp := 0.0;
        rAccelGridVoltageSp := 0.0;
        tArcRecoveryTimer(IN := TRUE, PT := T#2S);
        
        IF tArcRecoveryTimer.Q THEN
            tArcRecoveryTimer(IN := FALSE);
            iState := 30; (* Re-ignite *)
        END_IF;
        
    999: (* LATCHED FAULT STATE *)
        bSystemReady := FALSE;
        rScreenGridVoltageSp := 0.0;
        rAccelGridVoltageSp := 0.0;
        rXenonFlowValvePos := 0.0;
        rNeutralizerHeaterPwr := 0.0;
        (* Requires hardware reset, no automatic exit from fault *)

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
