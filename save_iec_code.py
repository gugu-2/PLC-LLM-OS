import json
import uuid
import os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Automated Vertical Form Fill Seal (VFFS) High-Speed Lyophilized Powder Packaging**

Task: Invent a highly complex, ultra-realistic control scenario for this domain (e.g., Servomotor electronic cam profile synchronization, auger doser weight feedback auto-tuning, and ultrasonic longitudinal seal fault tracking). Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_VFFS_PowderPackaging\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Automated Vertical Form Fill Seal (VFFS) High-Speed Lyophilized Powder Packaging

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_VFFS_PowderPackaging
(* 
   Advanced VFFS (Vertical Form Fill Seal) Control for Lyophilized Powder
   Features: Servo Cam Sync, Auger Doser PID Tuning, Ultrasonic Seal Tracking
*)
VAR_INPUT
    (* Safety and Enable Interlocks *)
    bSystemEnable           : BOOL;     (* Main system enable command *)
    bEmergencyStop          : BOOL;     (* E-Stop safety relay healthy status *)
    bGuardDoorsClosed       : BOOL;     (* Interlocking guard doors limit switches *)
    
    (* Process Variables *)
    rAugerWeightFeedback    : REAL;     (* Feedback from checkweigher in grams *)
    rFilmTensionActual      : REAL;     (* Current film tension feedback in N *)
    rSealTempActual         : REAL;     (* Longitudinal seal temperature feedback in °C *)
    rEncoderMasterPos       : REAL;     (* Master virtual axis position in degrees (0-360) *)
    
    (* Parameters *)
    rTargetWeight           : REAL := 50.0; (* Target powder dose weight in grams *)
    rSealTempSetpoint       : REAL := 185.0;(* Target ultrasonic seal temperature °C *)
END_VAR

VAR_OUTPUT
    (* Status and Control Outputs *)
    bSystemReady            : BOOL;     (* System is homed, heated, and ready to run *)
    bFaultAlarm             : BOOL;     (* Global fault flag *)
    iCurrentState           : INT;      (* Current state machine step index *)
    
    (* Actuator Commands *)
    rAugerSpeedCmd          : REAL;     (* RPM command to auger servomotor *)
    rFilmPullCamSlavePos    : REAL;     (* Slave position command for film pull servo *)
    rUltrasonicSealPower    : REAL;     (* Power command to longitudinal seal generator (0-100%) *)
    bJawCloseCmd            : BOOL;     (* Command to close transverse sealing jaws *)
END_VAR

VAR
    (* Internal State *)
    iState                  : INT := 0;
    
    (* Timers and Filters *)
    tSealTimer              : TON;
    tDoseTimer              : TON;
    rWeightErrorInt         : REAL := 0.0;
    rWeightErrorPrev        : REAL := 0.0;
    rWeightFiltered         : REAL := 0.0;
    
    (* Control Parameters *)
    rKp                     : REAL := 1.2;
    rKi                     : REAL := 0.05;
    rKd                     : REAL := 0.1;
    rBaseAugerSpeed         : REAL := 150.0;
    
    (* Fault Tracking *)
    iTempFaultCount         : INT := 0;
    bTempFault              : BOOL := FALSE;
END_VAR

(* === MAIN LOGIC === *)

(* 1. Safety and Interlock Check *)
IF NOT bEmergencyStop OR NOT bGuardDoorsClosed THEN
    bSystemReady := FALSE;
    bFaultAlarm := TRUE;
    rAugerSpeedCmd := 0.0;
    rUltrasonicSealPower := 0.0;
    bJawCloseCmd := FALSE;
    iState := 999; (* Fault state *)
    RETURN;
END_IF;

(* 2. Sensor Filtering (Low Pass Filter for Checkweigher) *)
rWeightFiltered := rWeightFiltered * 0.8 + rAugerWeightFeedback * 0.2;

(* 3. Main State Machine *)
CASE iState OF
    0: (* IDLE & INITIALIZATION *)
        bSystemReady := FALSE;
        bFaultAlarm := FALSE;
        rUltrasonicSealPower := 0.0;
        bJawCloseCmd := FALSE;
        
        IF bSystemEnable THEN
            iState := 10;
        END_IF;
        
    10: (* HEAT UP WARMING PHASE *)
        (* Simple P-control for ultrasonic block heating phase *)
        IF rSealTempActual < rSealTempSetpoint THEN
            rUltrasonicSealPower := (rSealTempSetpoint - rSealTempActual) * 2.5;
            IF rUltrasonicSealPower > 100.0 THEN
                rUltrasonicSealPower := 100.0;
            END_IF;
        ELSE
            rUltrasonicSealPower := 10.0; (* Maintain power *)
            bSystemReady := TRUE;
            iState := 20;
        END_IF;
        
    20: (* READY TO RUN / PRODUCTION MODE *)
        bSystemReady := TRUE;
        
        (* Electronic Cam profile for Film Puller relative to Master Encoder *)
        IF rEncoderMasterPos < 180.0 THEN
            (* Accelerate and pull film *)
            rFilmPullCamSlavePos := rEncoderMasterPos * 1.5;
        ELSE
            (* Dwell phase for sealing *)
            rFilmPullCamSlavePos := 270.0;
        END_IF;
        
        (* Trigger Dosing based on Master Angle *)
        IF (rEncoderMasterPos > 10.0) AND (rEncoderMasterPos < 15.0) THEN
            iState := 30;
        END_IF;

    30: (* DOSING PHASE WITH PID WEIGHT CORRECTION *)
        (* Calculate PID output for auger speed adjustment *)
        rWeightErrorInt := rWeightErrorInt + (rTargetWeight - rWeightFiltered);
        rAugerSpeedCmd := rBaseAugerSpeed 
                        + (rKp * (rTargetWeight - rWeightFiltered)) 
                        + (rKi * rWeightErrorInt) 
                        + (rKd * ((rTargetWeight - rWeightFiltered) - rWeightErrorPrev));
                        
        rWeightErrorPrev := (rTargetWeight - rWeightFiltered);
        
        tDoseTimer(IN := TRUE, PT := T#500MS);
        IF tDoseTimer.Q THEN
            tDoseTimer(IN := FALSE);
            rAugerSpeedCmd := 0.0;
            iState := 40;
        END_IF;
        
    40: (* TRANSVERSE SEAL AND CUT *)
        bJawCloseCmd := TRUE;
        tSealTimer(IN := TRUE, PT := T#300MS);
        
        IF tSealTimer.Q THEN
            bJawCloseCmd := FALSE;
            tSealTimer(IN := FALSE);
            
            (* Transition back to ready phase if still enabled *)
            IF bSystemEnable THEN
                iState := 20;
            ELSE
                iState := 0;
            END_IF;
        END_IF;
        
    999: (* FAULT HANDLING *)
        bSystemReady := FALSE;
        IF bSystemEnable = FALSE AND bEmergencyStop AND bGuardDoorsClosed THEN
            (* Reset fault if system disabled and safeties are clear *)
            bFaultAlarm := FALSE;
            iState := 0;
        END_IF;

END_CASE;

(* 4. Fault tracking and limits *)
IF ABS(rSealTempActual - rSealTempSetpoint) > 20.0 THEN
    iTempFaultCount := iTempFaultCount + 1;
    IF iTempFaultCount > 100 THEN
        bTempFault := TRUE;
        iState := 999;
    END_IF;
ELSE
    iTempFaultCount := 0;
    bTempFault := FALSE;
END_IF;

iCurrentState := iState;

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
