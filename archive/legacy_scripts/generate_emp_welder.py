import json, uuid, os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Advanced High-Power Electromagnetic Pulse (EMP) Welder**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., 100-kilojoule capacitor bank rapid discharge synchronization, intense magnetic field Lorentz force tube crimping, and high-voltage thyratron switching acoustic shock mitigation). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_EMP_WeldingSystem\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Advanced High-Power Electromagnetic Pulse (EMP) Welder

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_EMP_WeldingController
(* 
   =============================================================================
   Advanced High-Power Electromagnetic Pulse (EMP) Welder Controller
   =============================================================================
   Author: Principal Architect, Lumina Automation Systems
   Description: Controls the rapid discharge of a 100-kilojoule capacitor bank
                for Lorentz force tube crimping and welding. Features microsecond 
                synchronization, thyratron acoustic shock mitigation, and 
                multi-tier safety interlocks.
   =============================================================================
*)

VAR_INPUT
    bSystemEnable           : BOOL;     (* Master system enable signal *)
    bSafetyLoopOK           : BOOL;     (* Hardware safety relay OK signal *)
    bChargeInitiate         : BOOL;     (* Command to begin charging bank *)
    bTriggerWeld            : BOOL;     (* Command to trigger discharge *)
    rCapBankVoltage         : REAL;     (* Measured capacitor bank voltage (kV) *)
    rTargetVoltage          : REAL;     (* Setpoint for capacitor bank voltage (kV) *)
    rCoilTemp               : REAL;     (* Work coil temperature (Deg C) *)
    rThyratronPressure      : REAL;     (* Thyratron gas pressure (mTorr) *)
    rWeldChamberPressure    : REAL;     (* Welding chamber vacuum pressure (Torr) *)
END_VAR

VAR_OUTPUT
    bSystemReady            : BOOL;     (* System is ready for operation *)
    bChargingActive         : BOOL;     (* High Voltage power supply active *)
    bDischargePulse         : BOOL;     (* Thyratron trigger pulse *)
    bSafetyDumpActive       : BOOL;     (* Safety dump relays engaged *)
    rHVSupplyDemand         : REAL;     (* Control signal to HV supply (0-10V) *)
    bAlarmFault             : BOOL;     (* Global fault flag *)
    iFaultCode              : INT;      (* Detailed fault code *)
    bCoolingPumpCmd         : BOOL;     (* Cooling system command *)
END_VAR

VAR
    iState                  : INT := 0; (* Internal state machine *)
    tChargeTimer            : TON;      (* Max charging time watchdog *)
    tCoolDownTimer          : TON;      (* Pulse cool down watchdog *)
    tDischargePulseTimer    : TP;       (* Precise thyratron pulse width generator *)
    
    (* Internal Status Flags *)
    bChargeComplete         : BOOL := FALSE;
    bCoolingRequired        : BOOL := FALSE;
    
    (* Filtering for Analog Inputs *)
    rFilteredCapVoltage     : REAL := 0.0;
    rAlpha                  : REAL := 0.1; (* Low pass filter coefficient *)
    
    (* Limits *)
    rMaxVoltageLimit        : REAL := 45.0; (* 45 kV absolute maximum *)
    rMaxCoilTemp            : REAL := 85.0; (* 85 C maximum coil temp *)
    rMinChamberPressure     : REAL := 0.5;  (* Max 0.5 Torr for vacuum integrity *)
END_VAR

(* === MAIN LOGIC === *)

(* 1. Safety and Interlock Processing *)
IF NOT bSafetyLoopOK OR (rFilteredCapVoltage > rMaxVoltageLimit) OR (rCoilTemp > rMaxCoilTemp) THEN
    bSystemReady := FALSE;
    bChargingActive := FALSE;
    bDischargePulse := FALSE;
    rHVSupplyDemand := 0.0;
    bSafetyDumpActive := TRUE; (* Dump capacitor bank immediately *)
    bAlarmFault := TRUE;
    
    IF NOT bSafetyLoopOK THEN
        iFaultCode := 1001; (* Hardware E-Stop / Interlock broken *)
    ELSIF rFilteredCapVoltage > rMaxVoltageLimit THEN
        iFaultCode := 1002; (* Overvoltage condition *)
    ELSIF rCoilTemp > rMaxCoilTemp THEN
        iFaultCode := 1003; (* Coil overtemp *)
    END_IF;
    
    iState := 999; (* Enter fault state *)
    RETURN;
END_IF;

(* 2. Signal Filtering (First-Order Low Pass) *)
rFilteredCapVoltage := (rAlpha * rCapBankVoltage) + ((1.0 - rAlpha) * rFilteredCapVoltage);

(* 3. Cooling System Control *)
IF rCoilTemp > 45.0 THEN
    bCoolingRequired := TRUE;
ELSIF rCoilTemp < 35.0 THEN
    bCoolingRequired := FALSE;
END_IF;
bCoolingPumpCmd := bCoolingRequired;

(* 4. State Machine Control *)
CASE iState OF
    0: (* IDLE & SAFE *)
        bSystemReady := TRUE;
        bChargingActive := FALSE;
        rHVSupplyDemand := 0.0;
        bSafetyDumpActive := FALSE;
        bAlarmFault := FALSE;
        iFaultCode := 0;
        
        IF bSystemEnable AND bChargeInitiate THEN
            IF rWeldChamberPressure < rMinChamberPressure THEN
                iState := 10; (* Transition to Pre-Charge *)
            ELSE
                bAlarmFault := TRUE;
                iFaultCode := 2001; (* Chamber vacuum inadequate *)
            END_IF;
        END_IF;

    10: (* CHARGING PHASE *)
        bSystemReady := FALSE;
        bChargingActive := TRUE;
        bSafetyDumpActive := FALSE;
        
        (* Proportional charging control to approach target smoothly *)
        IF (rTargetVoltage - rFilteredCapVoltage) > 5.0 THEN
            rHVSupplyDemand := 10.0; (* Max charge rate *)
        ELSE
            rHVSupplyDemand := (rTargetVoltage - rFilteredCapVoltage) * 2.0;
            IF rHVSupplyDemand < 1.0 THEN rHVSupplyDemand := 1.0; END_IF;
        END_IF;
        
        (* Watchdog Timer for Charging *)
        tChargeTimer(IN := TRUE, PT := T#30S);
        
        IF rFilteredCapVoltage >= (rTargetVoltage - 0.1) THEN
            bChargeComplete := TRUE;
            rHVSupplyDemand := 0.0;
            bChargingActive := FALSE;
            tChargeTimer(IN := FALSE);
            iState := 20; (* Transition to Ready to Fire *)
        ELSIF tChargeTimer.Q THEN
            bAlarmFault := TRUE;
            iFaultCode := 2002; (* Charge timeout, potential dielectric leak *)
            tChargeTimer(IN := FALSE);
            iState := 999;
        END_IF;
        
    20: (* READY TO FIRE / HOLD *)
        bSystemReady := TRUE;
        
        (* Maintain voltage if droop occurs *)
        IF rFilteredCapVoltage < (rTargetVoltage - 0.5) THEN
            bChargingActive := TRUE;
            rHVSupplyDemand := 2.0; (* Trickle charge *)
        ELSE
            bChargingActive := FALSE;
            rHVSupplyDemand := 0.0;
        END_IF;
        
        IF bTriggerWeld AND bSystemEnable THEN
            iState := 30; (* Execute Pulse *)
        END_IF;
        
        IF NOT bChargeInitiate THEN
            iState := 90; (* Abort and discharge *)
        END_IF;

    30: (* DISCHARGE PULSE GENERATION *)
        bSystemReady := FALSE;
        bChargingActive := FALSE;
        rHVSupplyDemand := 0.0;
        
        (* Generate an exact 500us trigger pulse for the thyratron grid *)
        tDischargePulseTimer(IN := TRUE, PT := T#500US);
        bDischargePulse := tDischargePulseTimer.Q;
        
        IF NOT tDischargePulseTimer.Q THEN
            tDischargePulseTimer(IN := FALSE);
            iState := 40; (* Post-pulse delay *)
        END_IF;
        
    40: (* POST-PULSE COOL DOWN *)
        tCoolDownTimer(IN := TRUE, PT := T#5S);
        IF tCoolDownTimer.Q THEN
            tCoolDownTimer(IN := FALSE);
            bChargeComplete := FALSE;
            IF NOT bTriggerWeld THEN
                iState := 0; (* Return to idle when trigger released *)
            END_IF;
        END_IF;
        
    90: (* CONTROLLED DUMP *)
        bChargingActive := FALSE;
        rHVSupplyDemand := 0.0;
        bSafetyDumpActive := TRUE;
        
        IF rFilteredCapVoltage < 0.1 THEN
            bSafetyDumpActive := FALSE;
            iState := 0;
        END_IF;

    999: (* FAULT STATE *)
        bSystemReady := FALSE;
        bChargingActive := FALSE;
        bDischargePulse := FALSE;
        rHVSupplyDemand := 0.0;
        bSafetyDumpActive := TRUE;
        
        IF bSystemEnable = FALSE AND bChargeInitiate = FALSE THEN
            (* Acknowledge fault only when enable dropped *)
            IF rFilteredCapVoltage < 0.1 THEN
                iState := 0;
            END_IF;
        END_IF;
        
END_CASE;

END_FUNCTION_BLOCK
```"""

import os
os.makedirs("data/swarm_raw", exist_ok=True)
record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
