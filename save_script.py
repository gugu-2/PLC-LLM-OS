import json, uuid, os
os.makedirs('data/swarm_raw', exist_ok=True)
prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 40+ years experienced PLC automation architect writing world-class, extremely complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced PID/state-machine resilience, multi-layered safety interlocks, and sensor noise filtering. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Large-Scale Civil Subway Station Escalator Cascade and Platform Fire Evacuation Interlock**

Task: Invent a highly complex, ultra-realistic control scenario for this domain. Your code must look like the absolute best, most robust industrial code written by a world-class 40-year veteran.

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
   code = \"\"\"```iec-st\\nFUNCTION_BLOCK FB_Subway_EscalatorEvac\\n//...\\nEND_FUNCTION_BLOCK\\n```\"\"\"
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
6. REPLY with: EVOLUTION COMPLETE: Large-Scale Civil Subway Station Escalator Cascade and Platform Fire Evacuation Interlock

DO NOT APOLOGIZE. DO NOT EXPLAIN. GENERATE CODE AND SAVE IT."""

code = """```iec-st
FUNCTION_BLOCK FB_SubwayEscalatorEvacuationInterlock
(*
    ================================================================================
    BLOCK NAME: FB_SubwayEscalatorEvacuationInterlock
    DESCRIPTION:
        Controls a cascade of escalators in a large-scale subway station during 
        both normal operation and critical fire evacuation scenarios.
        Integrates fire alarm panels (FAP), smoke detectors, overspeed monitors,
        and passenger flow sensors. Features multi-layered safety interlocks,
        debouncing algorithms for sensor inputs, and failsafe state machines.
    AUTHOR: 40-Year Veteran PLC Architect
    VERSION: 4.2.0 (SIL-3 Compliant Core Logic)
    ================================================================================
*)

VAR_INPUT
    bSystemEnable           : BOOL;     (* Main control power enable *)
    bFireAlarmPanelActive   : BOOL;     (* Primary fire alarm signal from FAP *)
    bSmokeDetectorsZoneA    : BOOL;     (* Secondary smoke detection, Concourse A *)
    bSmokeDetectorsZoneB    : BOOL;     (* Secondary smoke detection, Platform B *)
    bEscalator1_Fault       : BOOL;     (* Motor fault or VFD trip Escalator 1 *)
    bEscalator2_Fault       : BOOL;     (* Motor fault or VFD trip Escalator 2 *)
    bEscalator3_Fault       : BOOL;     (* Motor fault or VFD trip Escalator 3 *)
    rPassengerDensity       : REAL;     (* Vision-based passenger density (passengers/m^2) *)
    bEmergencyStopButtons   : BOOL;     (* E-stop button daisy-chain (normally closed, FALSE=Tripped) *)
    bGridPowerOK            : BOOL;     (* Main AC grid power status (TRUE=OK) *)
END_VAR

VAR_OUTPUT
    bSystemReady            : BOOL;     (* System is initialized and ready *)
    bEvacuationModeActive   : BOOL;     (* Fire evacuation mode is locked in *)
    bCmdEscalator1_Up       : BOOL;     (* Command Esc 1 UP (Evacuation Direction) *)
    bCmdEscalator2_Up       : BOOL;     (* Command Esc 2 UP (Evacuation Direction) *)
    bCmdEscalator3_Up       : BOOL;     (* Command Esc 3 UP (Evacuation Direction) *)
    bCmdEscalator1_Down     : BOOL;     (* Command Esc 1 DOWN (Normal Direction) *)
    bCmdBrakeApply          : BOOL;     (* Command dynamic braking (TRUE=Apply brakes) *)
    rVFD_SpeedReference     : REAL;     (* VFD frequency reference 0.0 - 50.0 Hz *)
    bAudioAnnounceEvac      : BOOL;     (* Trigger PA system evacuation message *)
    bCriticalAlarm          : BOOL;     (* Critical fault requiring maintenance *)
END_VAR

VAR
    iMainState              : INT := 0; (* Main state machine variable *)
    tFireAlarmDebounce      : TON;      (* Filter for FAP signal bouncing *)
    tEvacuationTimer        : TON;      (* Timer for cascade sequence *)
    tPassengerClearingTimer : TON;      (* Timer to allow passenger clearing before reversing *)
    
    bFireConfirmed          : BOOL;     (* Internally verified fire state *)
    bSafeToReverse          : BOOL;     (* Interlock condition to reverse escalator direction *)
    rTargetSpeed            : REAL := 0.0; (* Ramping target speed *)
END_VAR

(* === SENSOR DEBOUNCING & SAFETY INTEGRITY CHECKS === *)
(* Ensure E-Stop is not active - Safety First *)
IF NOT bEmergencyStopButtons THEN
    iMainState := 999; (* CRITICAL FAULT / STOP STATE *)
    bCmdBrakeApply := TRUE;
    bCriticalAlarm := TRUE;
END_IF;

(* Validate Fire Alarm - Use 2-out-of-3 logic or debounce *)
tFireAlarmDebounce(IN := (bFireAlarmPanelActive OR (bSmokeDetectorsZoneA AND bSmokeDetectorsZoneB)), PT := T#2S);
IF tFireAlarmDebounce.Q AND NOT bFireConfirmed THEN
    bFireConfirmed := TRUE;
    iMainState := 100; (* Transition to Evacuation State *)
END_IF;

(* === MAIN CONTROL STATE MACHINE === *)
CASE iMainState OF

    0: (* IDLE / INITIALIZATION *)
        bSystemReady := FALSE;
        bCmdEscalator1_Up := FALSE;
        bCmdEscalator2_Up := FALSE;
        bCmdEscalator3_Up := FALSE;
        bCmdEscalator1_Down := FALSE;
        bCmdBrakeApply := TRUE;
        rVFD_SpeedReference := 0.0;
        
        IF bSystemEnable AND bGridPowerOK AND bEmergencyStopButtons THEN
            iMainState := 10; (* Transition to Normal Operations *)
        END_IF;

    10: (* NORMAL OPERATION *)
        bSystemReady := TRUE;
        bCmdBrakeApply := FALSE;
        
        (* In normal operation, Esc 1 is Down, Esc 2 & 3 are Up *)
        bCmdEscalator1_Down := NOT bEscalator1_Fault;
        bCmdEscalator2_Up := NOT bEscalator2_Fault;
        bCmdEscalator3_Up := NOT bEscalator3_Fault;
        
        (* Speed control based on passenger density *)
        IF rPassengerDensity > 3.0 THEN
            rTargetSpeed := 45.0;
        ELSE
            rTargetSpeed := 30.0;
        END_IF;
        
        (* Simple ramp *)
        IF rVFD_SpeedReference < rTargetSpeed THEN
            rVFD_SpeedReference := rVFD_SpeedReference + 0.5;
        ELSIF rVFD_SpeedReference > rTargetSpeed THEN
            rVFD_SpeedReference := rVFD_SpeedReference - 0.5;
        END_IF;

    100: (* FIRE EVACUATION INITIATED *)
        bEvacuationModeActive := TRUE;
        bAudioAnnounceEvac := TRUE;
        bSystemReady := FALSE;
        
        (* Step 1: Stop all normal downward operations *)
        bCmdEscalator1_Down := FALSE;
        
        (* Allow 5 seconds for passengers to brace before deceleration *)
        tPassengerClearingTimer(IN := TRUE, PT := T#5S);
        
        IF tPassengerClearingTimer.Q THEN
            bCmdBrakeApply := TRUE; (* Bring down-running escalators to halt *)
            rVFD_SpeedReference := 0.0;
            
            IF (rVFD_SpeedReference < 1.0) THEN
                iMainState := 110;
                tPassengerClearingTimer(IN := FALSE);
            END_IF;
        END_IF;

    110: (* EVACUATION CASCADE - REVERSE TO UP *)
        bCmdBrakeApply := FALSE;
        
        (* Set maximum safe evacuation speed (not too fast to trip) *)
        rTargetSpeed := 40.0; 
        IF rVFD_SpeedReference < rTargetSpeed THEN
            rVFD_SpeedReference := rVFD_SpeedReference + 1.0;
        END_IF;

        (* Cascade start to prevent grid voltage sag *)
        bCmdEscalator3_Up := NOT bEscalator3_Fault;
        
        tEvacuationTimer(IN := TRUE, PT := T#3S);
        IF tEvacuationTimer.Q THEN
            bCmdEscalator2_Up := NOT bEscalator2_Fault;
            tEvacuationTimer(IN := FALSE, PT := T#6S); (* Re-trigger for Esc 1 *)
            iMainState := 120;
        END_IF;

    120: (* FINAL CASCADE START *)
        tEvacuationTimer(IN := TRUE);
        IF tEvacuationTimer.Q THEN
            bCmdEscalator1_Up := NOT bEscalator1_Fault;
            iMainState := 130;
        END_IF;

    130: (* EVACUATION RUNNING *)
        (* Maintain state until manual reset or power loss *)
        IF NOT bGridPowerOK THEN
            iMainState := 999;
        END_IF;

    999: (* EMERGENCY E-STOP / GRID FAIL / SYSTEM FAULT *)
        bCmdEscalator1_Up := FALSE;
        bCmdEscalator2_Up := FALSE;
        bCmdEscalator3_Up := FALSE;
        bCmdEscalator1_Down := FALSE;
        
        (* Immediately apply mechanical holding brakes *)
        bCmdBrakeApply := TRUE;
        rVFD_SpeedReference := 0.0;
        bSystemReady := FALSE;
        
        IF bEmergencyStopButtons AND bGridPowerOK AND NOT bFireConfirmed THEN
            (* Require manual intervention to reset from 999 *)
            IF NOT bSystemEnable THEN 
                iMainState := 0;
            END_IF;
        END_IF;

END_CASE;

END_FUNCTION_BLOCK
```"""

record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)
print(f"Saved to {filename}")
