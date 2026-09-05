import os, json, uuid

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, and mathematically rigorous code.

**Your assigned domain is: Heavy-Duty Geothermal Well Drilling Mud Pump Matrix**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., high-pressure triplex pump phase synchronization, annular blowout preventer (BOP) acoustic feed-forward, and drilling fluid rheology viscosity looping). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_GeothermalMudPump\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Heavy-Duty Geothermal Well Drilling Mud Pump Matrix

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_GeothermalMudPumpMatrix
VAR_INPUT
    (* Core operational and safety signals *)
    bEnableMaster        : BOOL;      (* Master enable for mud pump matrix operation *)
    bEmergencyStop       : BOOL;      (* Safety relay OK signal (E-Stop, active low) *)
    
    (* Primary process variables *)
    rInletPressure       : REAL;      (* Mud suction inlet pressure [bar] *)
    rDischargePressure   : REAL;      (* High pressure discharge to wellbore [bar] *)
    rMudDensity          : REAL;      (* Drilling fluid density [sg] *)
    rMudViscosity        : REAL;      (* Mud rheological viscosity [cP] *)
    
    (* Advanced synchronization and target signals *)
    rFlowRateTarget      : REAL;      (* Target drilling fluid flow rate [L/min] *)
    rCylinder1Pos        : REAL;      (* Triplex pump cylinder 1 stroke position [mm] *)
    rAcousticFeedFwd     : REAL;      (* Annular BOP acoustic feed-forward magnitude *)
END_VAR
VAR_OUTPUT
    (* Status and control signals *)
    bSystemReady         : BOOL;      (* Mud pump matrix ready status *)
    rMotorSpeedRef       : REAL;      (* Triplex pump VFD speed reference [RPM] *)
    rBypassValveCmd      : REAL;      (* Annular bypass valve position command [%] *)
    bHighPressureAlarm   : BOOL;      (* Discharge pressure critical alarm *)
    bCavitationWarning   : BOOL;      (* Inlet cavitation risk warning *)
    rStrokeRateActual    : REAL;      (* Calculated stroke rate [SPM] *)
END_VAR
VAR
    (* Internal State Machine and Timers *)
    iMatrixState         : INT := 0;  (* Internal State Machine for sequencing *)
    tStartupDelay        : TON;       (* Startup sequence delay timer *)
    tViscosityFilter     : TON;       (* Filter delay for rheology changes *)
    
    (* PI Controller variables *)
    rPressureError       : REAL := 0.0;
    rPressureIntegral    : REAL := 0.0;
    rKp                  : REAL := 2.75;
    rKi                  : REAL := 0.22;
    
    (* Configurable operational limits *)
    rMaxDischargePress   : REAL := 380.0; (* Geothermal well max pressure [bar] *)
    rMinInletPress       : REAL := 2.5;   (* Minimum suction pressure to prevent cavitation [bar] *)
    rMaxMotorSpeed       : REAL := 1800.0;(* Max speed for the pump drive [RPM] *)
END_VAR

(* === MAIN LOGIC === *)
(* Emergency and Safety Interlocks: highest priority check *)
IF NOT bEmergencyStop THEN
    bSystemReady := FALSE;
    rMotorSpeedRef := 0.0;
    rBypassValveCmd := 100.0; (* Fail-safe open to relieve pressure immediately *)
    bHighPressureAlarm := TRUE;
    iMatrixState := 999; (* Enter Fault state *)
    RETURN;
END_IF;

(* Cavitation Protection Logic based on Inlet Pressure *)
IF rInletPressure < rMinInletPress THEN
    bCavitationWarning := TRUE;
ELSE
    bCavitationWarning := FALSE;
END_IF;

(* Discharge Pressure monitoring and Critical Alarming *)
IF rDischargePressure >= rMaxDischargePress THEN
    bHighPressureAlarm := TRUE;
ELSE
    bHighPressureAlarm := FALSE;
END_IF;

(* Main Control State Machine *)
CASE iMatrixState OF
    0: (* IDLE - Waiting for start command *)
        bSystemReady := TRUE;
        rMotorSpeedRef := 0.0;
        rBypassValveCmd := 100.0; (* Fully bypass flow during idle *)
        IF bEnableMaster AND NOT bHighPressureAlarm THEN
            iMatrixState := 10;
        END_IF;
        
    10: (* PRIMING - Build up suction pressure *)
        bSystemReady := FALSE;
        rBypassValveCmd := 50.0; (* Partially close bypass to prime *)
        tStartupDelay(IN := TRUE, PT := T#10S);
        IF tStartupDelay.Q THEN
            tStartupDelay(IN := FALSE);
            iMatrixState := 20;
        END_IF;
        
    20: (* RAMP_UP - Increase motor speed gradually for triplex pump *)
        rBypassValveCmd := 0.0; (* Close bypass completely for main flow *)
        rMotorSpeedRef := rMotorSpeedRef + 8.5; (* Soft ramp up rate *)
        
        (* Transition to PID control once we reach minimum operational speed *)
        IF rMotorSpeedRef >= (rFlowRateTarget * 0.45) THEN 
            iMatrixState := 30;
        END_IF;
        
        (* Check for disable command *)
        IF NOT bEnableMaster THEN
            iMatrixState := 0;
        END_IF;
        
    30: (* PID_CONTROL - Maintain flow and manage discharge pressure dynamically *)
        (* Calculate pressure error based on target and actual discharge pressure *)
        (* In this configuration, we modulate speed to maintain an equivalent target *)
        rPressureError := rFlowRateTarget - rDischargePressure; 
        
        (* Calculate Integral term with anti-windup clamping *)
        rPressureIntegral := rPressureIntegral + (rPressureError * 0.1);
        IF rPressureIntegral > 800.0 THEN rPressureIntegral := 800.0; END_IF;
        IF rPressureIntegral < -200.0 THEN rPressureIntegral := -200.0; END_IF;
        
        (* PI output calculation for Motor Speed Reference *)
        rMotorSpeedRef := (rKp * rPressureError) + (rKi * rPressureIntegral);
        
        (* Implement Acoustic Feed-Forward for Annular BOP mitigation *)
        IF rAcousticFeedFwd > 10.0 THEN
            rMotorSpeedRef := rMotorSpeedRef - (rAcousticFeedFwd * 0.5);
        END_IF;
        
        (* Limit motor speed to safe bounds *)
        IF rMotorSpeedRef > rMaxMotorSpeed THEN
            rMotorSpeedRef := rMaxMotorSpeed;
        ELSIF rMotorSpeedRef < 0.0 THEN
            rMotorSpeedRef := 0.0;
        END_IF;
        
        (* Advanced Rheology Feed-Forward Adaptation *)
        IF rMudViscosity > 65.0 THEN
            (* Increase torque/speed compensation for high viscosity mud *)
            rMotorSpeedRef := rMotorSpeedRef * 1.08; 
        END_IF;
        
        (* Stroke rate calculation based on speed and mechanical gear ratio *)
        rStrokeRateActual := rMotorSpeedRef / 14.8;
        
        (* State exit condition *)
        IF NOT bEnableMaster THEN
            iMatrixState := 0;
        END_IF;
        
    999: (* FAULT STATE - System requires reset *)
        bSystemReady := FALSE;
        rMotorSpeedRef := 0.0;
        rBypassValveCmd := 100.0;
        IF bEmergencyStop AND NOT bHighPressureAlarm AND NOT bEnableMaster THEN
            iMatrixState := 0; (* Reset only when safe and start signal cleared *)
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

filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Saved to {filename}")
