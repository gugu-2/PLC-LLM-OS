import os
import json
import uuid

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Molten Salt Solar Thermal Tower Central Receiver**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 565°C molten salt receiver temperature gradient control, cold/hot storage tank volume balancing, rapid transient cloud cover flow-rate adaptation, and anti-freeze trace heating interlocks). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_SolarThermalReceiver\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Molten Salt Solar Thermal Tower Central Receiver

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_MoltenSaltCentralReceiverCtrl
VAR_INPUT
    (* System operation signals *)
    bEnable                 : BOOL;     (* System master enable signal *)
    bEmergencyStop          : BOOL;     (* Hardwired emergency stop and safety loop OK (Active High) *)
    bCloudTransientFlag     : BOOL;     (* Advanced sky imager detection of incoming cloud cover *)
    
    (* Process measurements *)
    rSaltInletTemp          : REAL;     (* Receiver cold salt inlet temperature (deg C) *)
    rSaltOutletTemp         : REAL;     (* Receiver hot salt outlet temperature (deg C) *)
    rDniSensor              : REAL;     (* Direct Normal Irradiance from weather station (W/m^2) *)
    rColdTankLevel          : REAL;     (* Cold salt storage tank level (%) *)
    rHotTankLevel           : REAL;     (* Hot salt storage tank level (%) *)
    rReceiverFlowRate       : REAL;     (* Current molten salt mass flow rate (kg/s) *)
END_VAR
VAR_OUTPUT
    (* System Status *)
    bSystemReady            : BOOL;     (* Interlocks met, receiver ready for flux *)
    bAlarm                  : BOOL;     (* General fault or alarm active *)
    iCurrentState           : INT;      (* Current state machine step *)
    
    (* Actuator Commands *)
    rReceiverPumpSpeedCmd   : REAL;     (* Commanded VFD frequency for cold salt pump (Hz, 0-60) *)
    bHeliostatDefocusCmd    : BOOL;     (* Command to heliostat field controller to execute emergency defocus *)
    bTraceHeatingCmd        : BOOL;     (* Activate electrical trace heating to prevent salt freeze *)
    bDrainValveCmd          : BOOL;     (* Command to open receiver drain valves (failsafe open) *)
END_VAR
VAR
    (* Internal State & Timers *)
    iState                  : INT := 0; 
    tPreheatTimer           : TON;
    tTransientTimer         : TON;
    tShutdownTimer          : TON;
    
    (* Control Constants & Internal Variables *)
    rTargetOutletTemp       : REAL := 565.0; (* Optimal molten salt design temperature *)
    rMaxSafeTemp            : REAL := 595.0; (* Structural limit of receiver tubes *)
    rFreezingLimitTemp      : REAL := 290.0; (* Freezing point of nitrate salt mixture + safety margin *)
    
    rCalculatedSetPoint     : REAL;
    rFlowError              : REAL;
    rKp                     : REAL := 1.25;
    rKi                     : REAL := 0.05;
    rIntegralAccumulator    : REAL := 0.0;
    
    bFreezeWarning          : BOOL;
    bOverTempWarning        : BOOL;
END_VAR

(* === MAIN LOGIC AND SAFETY INTERLOCKS === *)

(* Check for Emergency Stop or Critical Safety Faults *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    bAlarm := TRUE;
    bHeliostatDefocusCmd := TRUE; 
    rReceiverPumpSpeedCmd := 0.0;
    bDrainValveCmd := TRUE; (* Drain salt back to cold tank immediately *)
    bTraceHeatingCmd := TRUE; (* Maintain temp for residual salt *)
    iState := 999; (* FAULT STATE *)
    RETURN;
END_IF;

(* Continuous Monitoring for Freeze Risk *)
IF rSaltInletTemp < rFreezingLimitTemp OR rSaltOutletTemp < rFreezingLimitTemp THEN
    bFreezeWarning := TRUE;
    bTraceHeatingCmd := TRUE;
ELSE
    bFreezeWarning := FALSE;
    (* Keep trace heating active only if state requires it or during freeze warning *)
END_IF;

(* Continuous Monitoring for Over-temperature Risk *)
IF rSaltOutletTemp > rMaxSafeTemp THEN
    bOverTempWarning := TRUE;
    bHeliostatDefocusCmd := TRUE;
    bAlarm := TRUE;
ELSE
    bOverTempWarning := FALSE;
END_IF;

(* Core Central Receiver State Machine *)
CASE iState OF
    0: (* IDLE & STANDBY *)
        bSystemReady := FALSE;
        rReceiverPumpSpeedCmd := 0.0;
        bHeliostatDefocusCmd := TRUE; (* Field parked *)
        bDrainValveCmd := TRUE; (* Receiver drained *)
        bAlarm := FALSE;
        
        IF bEnable AND rColdTankLevel > 10.0 AND NOT bFreezeWarning THEN
            iState := 10; (* Transition to Pre-heat *)
        END_IF;

    10: (* PRE-HEAT SEQUENCE *)
        bSystemReady := FALSE;
        bDrainValveCmd := FALSE; (* Close drain valves to establish flow *)
        bTraceHeatingCmd := TRUE; (* Engage heaters *)
        
        (* Start pump at minimum speed to establish circulation *)
        rReceiverPumpSpeedCmd := 15.0; 
        
        tPreheatTimer(IN := TRUE, PT := T#5M);
        IF tPreheatTimer.Q AND (rSaltInletTemp > 300.0) THEN
            tPreheatTimer(IN := FALSE);
            iState := 20; (* Transition to Ready *)
        END_IF;
        
        IF NOT bEnable THEN
            tPreheatTimer(IN := FALSE);
            iState := 100; (* SHUTDOWN *)
        END_IF;

    20: (* READY FOR FLUX *)
        bSystemReady := TRUE;
        bTraceHeatingCmd := FALSE;
        bHeliostatDefocusCmd := FALSE; (* Permit field to focus on receiver *)
        
        (* Maintain minimum flow *)
        rReceiverPumpSpeedCmd := 20.0;
        
        IF rDniSensor > 250.0 AND rSaltOutletTemp > 350.0 THEN
            iState := 30; (* ACTIVE TRACKING AND HEATING *)
        END_IF;
        
        IF NOT bEnable THEN
            iState := 100;
        END_IF;

    30: (* ACTIVE TRACKING - ADVANCED PID FLOW CONTROL *)
        (* In this state, we modulate pump speed to maintain exactly 565C outlet *)
        
        rFlowError := rSaltOutletTemp - rTargetOutletTemp;
        
        (* Anti-windup for integral component *)
        IF rReceiverPumpSpeedCmd > 10.0 AND rReceiverPumpSpeedCmd < 60.0 THEN
            rIntegralAccumulator := rIntegralAccumulator + (rFlowError * rKi);
        END_IF;
        
        (* Proportional + Integral logic - Inverse acting because hotter temp needs MORE flow to cool *)
        rReceiverPumpSpeedCmd := 30.0 + (rFlowError * rKp) + rIntegralAccumulator;
        
        (* Clamp pump limits *)
        IF rReceiverPumpSpeedCmd < 15.0 THEN
            rReceiverPumpSpeedCmd := 15.0;
        ELSIF rReceiverPumpSpeedCmd > 60.0 THEN
            rReceiverPumpSpeedCmd := 60.0;
        END_IF;
        
        (* Handle DNI transients (Cloud cover prediction) *)
        IF bCloudTransientFlag THEN
            iState := 40;
        END_IF;
        
        IF NOT bEnable OR rHotTankLevel > 98.0 THEN
            iState := 100;
        END_IF;
        
    40: (* TRANSIENT MITIGATION (CLOUD COVER) *)
        (* Cloud shadow expected. Ramp down flow predictively to avoid temperature crashes *)
        rReceiverPumpSpeedCmd := 15.0; (* Drop to minimum safe circulation *)
        
        tTransientTimer(IN := TRUE, PT := T#30S);
        IF NOT bCloudTransientFlag AND tTransientTimer.Q THEN
            tTransientTimer(IN := FALSE);
            iState := 30; (* Resume normal operation *)
        END_IF;

    100: (* SHUTDOWN SEQUENCE *)
        bHeliostatDefocusCmd := TRUE;
        rReceiverPumpSpeedCmd := 60.0; (* Flush the receiver at high speed briefly *)
        
        tShutdownTimer(IN := TRUE, PT := T#2M);
        IF tShutdownTimer.Q THEN
            tShutdownTimer(IN := FALSE);
            bDrainValveCmd := TRUE; (* Open drains *)
            rReceiverPumpSpeedCmd := 0.0;
            iState := 0;
        END_IF;

    999: (* FAULT HANDLING *)
        (* Requires manual reset via bEnable toggle after emergency stop clears *)
        IF bEmergencyStop AND NOT bEnable THEN
            iState := 0;
        END_IF;
        
END_CASE;

iCurrentState := iState;

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
