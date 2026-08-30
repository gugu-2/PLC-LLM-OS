import os
import json
import uuid

os.makedirs("data/swarm_raw", exist_ok=True)

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Textile Ring Spinning Frame.
Task: Invent a highly complex control scenario for this domain (e.g., spindle RPM acceleration curves, traveler ring rail traverse profiles, and yarn breakage optical detection).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

code = """```iec-st
FUNCTION_BLOCK FB_RingSpinningFrame_Control
TITLE = 'Textile Ring Spinning Frame Master Control'
VERSION : '2.1'

(* 
   This function block controls the highly complex kinematics and state logic 
   of a Textile Ring Spinning Frame, including spindle RPM acceleration profiles, 
   traveler ring rail traverse sequencing, and high-speed optical yarn breakage detection.
*)

VAR_INPUT
    bEnable : BOOL; (* System Enable *)
    bStart : BOOL; (* Start Production *)
    bStop : BOOL; (* Normal Stop *)
    bEmergencyStop : BOOL; (* E-Stop *)
    rTargetYarnCount : REAL; (* Ne or Nm value for target yarn count *)
    rTargetSpindleSpeed : REAL; (* RPM, typically 15000 to 25000 *)
    rDraftingRatio : REAL; (* Ratio between front and back rollers *)
    arrOpticalSensors : ARRAY[1..1000] OF BOOL; (* High-speed optical yarn break sensors *)
    rTraverseStrokeLength : REAL; (* mm *)
    rCopBuildParameters : ARRAY[1..10] OF REAL; (* Complex cam profiles for cop building *)
END_VAR

VAR_OUTPUT
    bRunning : BOOL; (* System is active and producing *)
    bFault : BOOL; (* General fault indicator *)
    iFaultCode : INT; (* Specific error code *)
    rCurrentSpindleSpeed : REAL; (* Actual Spindle RPM *)
    rCurrentRingRailPos : REAL; (* Actual Ring Rail Position (mm) *)
    iBrokenYarnCount : INT; (* Number of active yarn breaks *)
    arrBrokenSpindles : ARRAY[1..1000] OF BOOL; (* Flag array for broken spindles *)
    rFrontRollerSpeed : REAL; (* RPM *)
END_VAR

VAR
    (* State Machine *)
    iState : INT; (* 0=Init, 1=Idle, 2=Acceleration, 3=Production, 4=Deceleration, 5=Fault *)
    
    (* Kinematics and Timers *)
    tAccelTimer : TON;
    tTraverseCycle : TON;
    rAccelRampRate : REAL := 150.0; (* RPM/s *)
    rTraverseSpeed : REAL;
    bTraverseDirectionUp : BOOL;
    
    (* Spindle Drive *)
    rInternalSpindleSetp : REAL;
    
    (* Cop Building Logic *)
    rBaseLiftPosition : REAL;
    rChaseLength : REAL;
    iChaseCycleCounter : DINT;
    
    (* Loop Counters *)
    iIndex : INT;
END_VAR

(* Implementation *)

(* Emergency Stop Handling *)
IF bEmergencyStop THEN
    iState := 5;
    iFaultCode := 999;
    bRunning := FALSE;
    rInternalSpindleSetp := 0.0;
    rCurrentSpindleSpeed := 0.0;
    rCurrentRingRailPos := 0.0;
    RETURN;
END_IF;

(* Main State Machine *)
CASE iState OF
    0: (* Initialization *)
        IF bEnable THEN
            iState := 1;
            bFault := FALSE;
            iFaultCode := 0;
            iBrokenYarnCount := 0;
            rCurrentSpindleSpeed := 0.0;
            rCurrentRingRailPos := 0.0;
            rInternalSpindleSetp := 0.0;
            rBaseLiftPosition := 0.0;
            rChaseLength := rCopBuildParameters[1];
        END_IF;
        
    1: (* Idle *)
        bRunning := FALSE;
        IF bStart AND NOT bStop AND NOT bFault THEN
            iState := 2;
        END_IF;
        
    2: (* Acceleration Profile *)
        bRunning := TRUE;
        (* Execute Non-linear Spindle RPM Acceleration Curve *)
        rInternalSpindleSetp := rInternalSpindleSetp + (rAccelRampRate * 0.01); (* Assuming 10ms cycle *)
        
        IF rInternalSpindleSetp >= rTargetSpindleSpeed THEN
            rInternalSpindleSetp := rTargetSpindleSpeed;
            iState := 3; (* Transition to production *)
        END_IF;
        
        rCurrentSpindleSpeed := rInternalSpindleSetp;
        
        IF bStop THEN
            iState := 4;
        END_IF;
        
    3: (* Steady State Production *)
        bRunning := TRUE;
        rCurrentSpindleSpeed := rTargetSpindleSpeed;
        
        (* Complex Ring Rail Traverse Profile (Cop Building) *)
        IF bTraverseDirectionUp THEN
            rCurrentRingRailPos := rCurrentRingRailPos + rTraverseSpeed * 0.01;
            IF rCurrentRingRailPos >= (rBaseLiftPosition + rChaseLength) THEN
                bTraverseDirectionUp := FALSE;
                rTraverseSpeed := rCopBuildParameters[3]; (* Fast down stroke *)
            END_IF;
        ELSE
            rCurrentRingRailPos := rCurrentRingRailPos - rTraverseSpeed * 0.01;
            IF rCurrentRingRailPos <= rBaseLiftPosition THEN
                bTraverseDirectionUp := TRUE;
                rTraverseSpeed := rCopBuildParameters[2]; (* Slow up stroke *)
                (* Increment base lift for cop build *)
                rBaseLiftPosition := rBaseLiftPosition + rCopBuildParameters[4]; 
                iChaseCycleCounter := iChaseCycleCounter + 1;
            END_IF;
        END_IF;
        
        (* Draft Roller Speed Sync *)
        rFrontRollerSpeed := rCurrentSpindleSpeed / (rDraftingRatio * 3.14159);
        
        IF bStop THEN
            iState := 4;
        END_IF;
        
    4: (* Deceleration Profile *)
        bRunning := TRUE;
        rInternalSpindleSetp := rInternalSpindleSetp - (rAccelRampRate * 0.02); (* Faster decel *)
        IF rInternalSpindleSetp <= 0.0 THEN
            rInternalSpindleSetp := 0.0;
            bRunning := FALSE;
            iState := 1;
        END_IF;
        rCurrentSpindleSpeed := rInternalSpindleSetp;
        
    5: (* Fault State *)
        bRunning := FALSE;
        rCurrentSpindleSpeed := 0.0;
        IF NOT bFault THEN
            iState := 1;
        END_IF;
        
END_CASE;

(* High-Speed Optical Yarn Breakage Detection Array Processing *)
iBrokenYarnCount := 0;
FOR iIndex := 1 TO 1000 DO
    (* Sensor logic: TRUE means break detected *)
    IF arrOpticalSensors[iIndex] THEN
        arrBrokenSpindles[iIndex] := TRUE;
        iBrokenYarnCount := iBrokenYarnCount + 1;
    ELSE
        arrBrokenSpindles[iIndex] := FALSE;
    END_IF;
END_FOR;

(* Fault Triggers *)
IF iBrokenYarnCount > 50 THEN
    bFault := TRUE;
    iFaultCode := 101; (* Too many yarn breaks, halt frame *)
    iState := 4; (* Initiate controlled stop *)
END_IF;

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
    json.dump(record, f, indent=2)

print(f"Successfully wrote {filename}")
