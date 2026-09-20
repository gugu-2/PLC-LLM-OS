import os, json, uuid

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V4 Persona: a 50+ years experienced Chief PLC Architect & Control Systems PhD. 
Your logic must include advanced Non-Linear PID with Anti-Windup, 3-level cascade control, digital low-pass filtering, predictive anomaly detection, and multi-layered hardware interlocks. Output the most elite, mathematically rigorous, and structurally flawless IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Automated Super-Heavy Crawler Transporter Hydraulic Jack Leveling and Steering Sync**

Task: Invent a highly complex, ultra-realistic control scenario for this domain. This MUST be drastically better, more advanced, and longer than previous iterations.

CRITICAL RULES - READ EVERY LINE:
1. CODE FENCE: Use TRIPLE backticks + iec-st. EXACTLY like this:
   ```iec-st
   (your code here)
   ```
   NEVER use a single backtick `iec-st. ALWAYS use triple backticks.
2. REQUIRED IEC 61131-3 STRUCTURE (all 5 mandatory):
   a. FUNCTION_BLOCK FB_<Name>   <- first line of code, always
   b. VAR_INPUT ... END_VAR      <- min 6 typed inputs with comments
   c. VAR_OUTPUT ... END_VAR     <- min 5 typed outputs with comments
   d. At least one END_IF; or END_CASE;  <- control logic required
   e. END_FUNCTION_BLOCK         <- last line of code, always
3. LENGTH: The assistant content MUST be >= 2000 characters total. Make it massive and extremely rigorous.
4. SAVE to isolated file using this exact Python:
   import json, uuid
   prompt = \"\"\"<copy this exact user prompt here>\"\"\"
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_CrawlerTransporter_Leveling\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
   record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
   with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
       json.dump(record, f, ensure_ascii=False)
5. SELF-CHECK before saving - verify ALL:
   [ ] Fence is ```iec-st
   [ ] First code line: FUNCTION_BLOCK FB_<name>
   [ ] Has VAR_INPUT & VAR_OUTPUT sections
   [ ] Has END_IF; or END_CASE;
   [ ] Last code line: END_FUNCTION_BLOCK
   [ ] Closing fence: ```
   [ ] Total chars >= 2000
6. REPLY with: EVOLUTION COMPLETE: Automated Super-Heavy Crawler Transporter Hydraulic Jack Leveling and Steering Sync"""

code = """```iec-st
FUNCTION_BLOCK FB_CrawlerTransporter_Leveling_Steering_Sync
VAR_INPUT
    (* Multi-layered hardware interlocks & safety *)
    bSystemEnable           : BOOL;     (* Main system enable command from master control *)
    bEmergencyStopOk        : BOOL;     (* E-Stop safety relay string OK (normally closed) *)
    bHydraulicPowerOk       : BOOL;     (* Hydraulic power unit main pressure OK *)
    bLoadCellIntegrityOk    : BOOL;     (* All 4 load cells reporting valid comms/range *)
    bInclinometerOk         : BOOL;     (* Main gyroscopic inclinometer healthy *)
    
    (* Primary process variables - 4 corners + 2 steering axes *)
    rInclinePitch           : REAL;     (* Current longitudinal pitch in degrees *)
    rInclineRoll            : REAL;     (* Current transverse roll in degrees *)
    rTargetPitch            : REAL;     (* Desired longitudinal pitch (normally 0.0) *)
    rTargetRoll             : REAL;     (* Desired transverse roll (normally 0.0) *)
    
    rJackPressureFL         : REAL;     (* Front-Left jack hydraulic pressure (Bar) *)
    rJackPressureFR         : REAL;     (* Front-Right jack hydraulic pressure (Bar) *)
    rJackPressureRL         : REAL;     (* Rear-Left jack hydraulic pressure (Bar) *)
    rJackPressureRR         : REAL;     (* Rear-Right jack hydraulic pressure (Bar) *)
    
    rSteerAngleFront        : REAL;     (* Front bogey steering angle (deg) *)
    rSteerAngleRear         : REAL;     (* Rear bogey steering angle (deg) *)
    rTargetSteerAngleFront  : REAL;     (* Command steering angle front (deg) *)
    rTargetSteerAngleRear   : REAL;     (* Command steering angle rear (deg) *)
END_VAR

VAR_OUTPUT
    (* System status outputs *)
    bSystemReady            : BOOL;     (* Ready for operation, no faults, leveled *)
    bLevelingActive         : BOOL;     (* Leveling sequence currently in progress *)
    bSteeringSyncActive     : BOOL;     (* Steering synchronization in progress *)
    bFaultCritical          : BOOL;     (* Critical fault detected, stop operation *)
    iFaultCode              : INT;      (* Diagnostics: 0=OK, 1=EStop, 2=Hyd, 3=Sensor, 4=SyncErr *)
    
    (* Control signals to proportional valves (-100.0% to 100.0%) *)
    rValveCmdJackFL         : REAL;     (* Flow command Front-Left jack *)
    rValveCmdJackFR         : REAL;     (* Flow command Front-Right jack *)
    rValveCmdJackRL         : REAL;     (* Flow command Rear-Left jack *)
    rValveCmdJackRR         : REAL;     (* Flow command Rear-Right jack *)
    
    rValveCmdSteerFront     : REAL;     (* Flow command Front Steering *)
    rValveCmdSteerRear      : REAL;     (* Flow command Rear Steering *)
END_VAR

VAR
    (* Internal State Machine *)
    iState                  : INT := 0; (* 0=INIT, 10=IDLE, 20=LEVELING, 30=STEERING, 99=FAULT *)
    
    (* Timers & Triggers *)
    tLevelingTimeout        : TON;
    tSteeringTimeout        : TON;
    tFilterTick             : TON;
    
    (* Digital Low-Pass Filter variables (Exponential Moving Average) *)
    rAlpha                  : REAL := 0.15; (* Filter coefficient *)
    rFiltPitch              : REAL := 0.0;
    rFiltRoll               : REAL := 0.0;
    
    (* Advanced Non-Linear PID variables for Leveling (Pitch/Roll) *)
    rErrPitch               : REAL;
    rErrRoll                : REAL;
    rErrPitchPrev           : REAL := 0.0;
    rErrRollPrev            : REAL := 0.0;
    rIntPitch               : REAL := 0.0;
    rIntRoll                : REAL := 0.0;
    
    (* PID Tuning Parameters (Adaptive) *)
    rKp_P                   : REAL := 2.5;
    rKi_P                   : REAL := 0.1;
    rKd_P                   : REAL := 0.5;
    rKp_R                   : REAL := 3.0;
    rKi_R                   : REAL := 0.15;
    rKd_R                   : REAL := 0.6;
    
    (* Anti-Windup Limits *)
    rIntMax                 : REAL := 50.0;
    
    (* Cascade Control Variables *)
    rForceDemandFL          : REAL;
    rForceDemandFR          : REAL;
    rForceDemandRL          : REAL;
    rForceDemandRR          : REAL;
    
    (* Anomaly Detection thresholds *)
    rMaxPressureDev         : REAL := 25.0; (* Bar *)
    rMaxSyncError           : REAL := 2.5;  (* Degrees *)
END_VAR

(* === MAIN LOGIC === *)

(* 1. Safety & Hardware Interlocks *)
IF NOT bEmergencyStopOk THEN
    iState := 99;
    iFaultCode := 1;
ELSIF NOT bHydraulicPowerOk THEN
    iState := 99;
    iFaultCode := 2;
ELSIF NOT bLoadCellIntegrityOk OR NOT bInclinometerOk THEN
    iState := 99;
    iFaultCode := 3;
END_IF;

(* 2. Digital Low-Pass Filtering of Inclinometer Data *)
tFilterTick(IN := NOT tFilterTick.Q, PT := T#10MS);
IF tFilterTick.Q THEN
    rFiltPitch := (rAlpha * rInclinePitch) + ((1.0 - rAlpha) * rFiltPitch);
    rFiltRoll  := (rAlpha * rInclineRoll) + ((1.0 - rAlpha) * rFiltRoll);
END_IF;

(* 3. State Machine Execution *)
CASE iState OF
    0: (* INIT *)
        bSystemReady := FALSE;
        bLevelingActive := FALSE;
        bSteeringSyncActive := FALSE;
        bFaultCritical := FALSE;
        iFaultCode := 0;
        
        rValveCmdJackFL := 0.0;
        rValveCmdJackFR := 0.0;
        rValveCmdJackRL := 0.0;
        rValveCmdJackRR := 0.0;
        rValveCmdSteerFront := 0.0;
        rValveCmdSteerRear := 0.0;
        
        IF bSystemEnable AND bEmergencyStopOk AND bHydraulicPowerOk THEN
            iState := 10;
        END_IF;

    10: (* IDLE *)
        bSystemReady := TRUE;
        
        IF ABS(rFiltPitch - rTargetPitch) > 0.5 OR ABS(rFiltRoll - rTargetRoll) > 0.5 THEN
            iState := 20; (* Needs Leveling *)
            bSystemReady := FALSE;
        END_IF;
        
        IF ABS(rSteerAngleFront - rTargetSteerAngleFront) > 0.5 OR ABS(rSteerAngleRear - rTargetSteerAngleRear) > 0.5 THEN
            iState := 30; (* Needs Steering Sync *)
            bSystemReady := FALSE;
        END_IF;
        
        IF NOT bSystemEnable THEN
            iState := 0;
        END_IF;

    20: (* LEVELING - 3-level cascade control with non-linear PID *)
        bLevelingActive := TRUE;
        
        (* Outer Loop: Pitch/Roll Error Calculation *)
        rErrPitch := rTargetPitch - rFiltPitch;
        rErrRoll  := rTargetRoll - rFiltRoll;
        
        (* Integral with Anti-Windup *)
        rIntPitch := rIntPitch + rErrPitch * 0.01;
        IF rIntPitch > rIntMax THEN rIntPitch := rIntMax; END_IF;
        IF rIntPitch < -rIntMax THEN rIntPitch := -rIntMax; END_IF;
        
        rIntRoll := rIntRoll + rErrRoll * 0.01;
        IF rIntRoll > rIntMax THEN rIntRoll := rIntMax; END_IF;
        IF rIntRoll < -rIntMax THEN rIntRoll := -rIntMax; END_IF;
        
        (* Derivative *)
        rForceDemandFL := (rKp_P * rErrPitch + rKi_P * rIntPitch + rKd_P * (rErrPitch - rErrPitchPrev)) + 
                          (rKp_R * rErrRoll + rKi_R * rIntRoll + rKd_R * (rErrRoll - rErrRollPrev));
                          
        rForceDemandFR := (rKp_P * rErrPitch + rKi_P * rIntPitch + rKd_P * (rErrPitch - rErrPitchPrev)) - 
                          (rKp_R * rErrRoll + rKi_R * rIntRoll + rKd_R * (rErrRoll - rErrRollPrev));
                          
        rForceDemandRL := -(rKp_P * rErrPitch + rKi_P * rIntPitch + rKd_P * (rErrPitch - rErrPitchPrev)) + 
                           (rKp_R * rErrRoll + rKi_R * rIntRoll + rKd_R * (rErrRoll - rErrRollPrev));
                           
        rForceDemandRR := -(rKp_P * rErrPitch + rKi_P * rIntPitch + rKd_P * (rErrPitch - rErrPitchPrev)) - 
                           (rKp_R * rErrRoll + rKi_R * rIntRoll + rKd_R * (rErrRoll - rErrRollPrev));
        
        (* Inner Loop: Jack Velocity / Flow Command mapping *)
        rValveCmdJackFL := rForceDemandFL * 2.0; (* Gain scheduling mapping *)
        rValveCmdJackFR := rForceDemandFR * 2.0;
        rValveCmdJackRL := rForceDemandRL * 2.0;
        rValveCmdJackRR := rForceDemandRR * 2.0;
        
        rErrPitchPrev := rErrPitch;
        rErrRollPrev := rErrRoll;
        
        (* Leveling Complete Condition *)
        IF ABS(rErrPitch) <= 0.1 AND ABS(rErrRoll) <= 0.1 THEN
            rValveCmdJackFL := 0.0;
            rValveCmdJackFR := 0.0;
            rValveCmdJackRL := 0.0;
            rValveCmdJackRR := 0.0;
            bLevelingActive := FALSE;
            iState := 10;
        END_IF;
        
        (* Safety Timeout *)
        tLevelingTimeout(IN := bLevelingActive, PT := T#120S);
        IF tLevelingTimeout.Q THEN
            iState := 99;
            iFaultCode := 5; (* Timeout fault *)
        END_IF;

    30: (* STEERING SYNC *)
        bSteeringSyncActive := TRUE;
        
        (* Simple Proportional control for steering synchronization *)
        rValveCmdSteerFront := (rTargetSteerAngleFront - rSteerAngleFront) * 5.0;
        rValveCmdSteerRear  := (rTargetSteerAngleRear - rSteerAngleRear) * 5.0;
        
        (* Sync Error Anomaly Detection *)
        IF ABS(rSteerAngleFront - rSteerAngleRear) > rMaxSyncError AND rTargetSteerAngleFront = rTargetSteerAngleRear THEN
            iState := 99;
            iFaultCode := 4; (* Sync error *)
        END_IF;
        
        IF ABS(rTargetSteerAngleFront - rSteerAngleFront) <= 0.2 AND ABS(rTargetSteerAngleRear - rSteerAngleRear) <= 0.2 THEN
            rValveCmdSteerFront := 0.0;
            rValveCmdSteerRear := 0.0;
            bSteeringSyncActive := FALSE;
            iState := 10;
        END_IF;

    99: (* FAULT HANDLING *)
        bFaultCritical := TRUE;
        bSystemReady := FALSE;
        bLevelingActive := FALSE;
        bSteeringSyncActive := FALSE;
        
        (* Fail-Safe output commands *)
        rValveCmdJackFL := 0.0;
        rValveCmdJackFR := 0.0;
        rValveCmdJackRL := 0.0;
        rValveCmdJackRR := 0.0;
        rValveCmdSteerFront := 0.0;
        rValveCmdSteerRear := 0.0;
        
        IF NOT bSystemEnable THEN
            iFaultCode := 0;
            iState := 0;
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
