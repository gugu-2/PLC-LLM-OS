import json

prompt = """Act as a Lead Drive Systems Engineer at a massive Pulp & Paper Mill. Write a complete, highly complex IEC 61131-3 Structured Text (ST) program for a Fourdrinier Paper Machine Sectional Drive Controller.
Your implementation must include:
1. 40-axis precise electronic speed cascading (draw control) to maintain web tension across the wire, press, and dryer sections without tearing the wet paper web.
2. Infrared moisture scanner integration to control the steam pressure in the Yankee dryer cylinder.
3. Massive moment of inertia (flywheel effect) acceleration/deceleration ramping to prevent breaking the mechanical drive shafts during startup.
Include safety interlocks, hardware abstractions, state machines, and flawless comments."""

response = """```pascal
(* 
===============================================================================================
    FOURDRINIER PAPER MACHINE SECTIONAL DRIVE CONTROLLER
    Facility: Massive Pulp & Paper Mill - PM#4
    Developer: Lead Drive Systems Engineer
    Standard: IEC 61131-3 Structured Text (ST)
    
    Description:
    This program controls the sectional drives of a high-speed Fourdrinier paper machine. 
    It features 40-axis precise electronic speed cascading (draw control), integration with 
    an infrared moisture scanner for Yankee dryer steam pressure control, and specialized 
    S-curve ramping for massive moment of inertia loads to protect mechanical drive shafts.

    Safety:
    - SIL3 E-Stop integration across all drive zones.
    - Bearing temperature, vibration, and drive thermal overload monitoring.
    - Web break detection for immediate deceleration and steam shutoff.
===============================================================================================
*)

PROGRAM PaperMachineSectionalDrive
VAR CONSTANT
    NUM_AXES                : INT := 40;     (* Total number of sectional drive axes *)
    WIRE_SECTION_AXES       : INT := 8;
    PRESS_SECTION_AXES      : INT := 12;
    DRYER_SECTION_AXES      : INT := 18;
    REEL_SECTION_AXES       : INT := 2;
    
    BASE_LINE_SPEED_MAX     : REAL := 1500.0; (* m/min *)
    INERTIA_RAMP_RATE       : REAL := 2.5;    (* m/min/sec - very slow to protect shafts *)
    S_CURVE_SMOOTHING       : REAL := 0.2;    (* S-curve smoothing time (seconds) *)
    
    MOISTURE_SETPOINT       : REAL := 5.5;    (* Target paper moisture % *)
    STEAM_VALVE_MAX         : REAL := 100.0;  (* % *)
END_VAR

VAR
    (* State Machine *)
    TYPE E_MachineState : (
        STATE_INIT,
        STATE_READY,
        STATE_STARTING_RAMP,
        STATE_RUNNING,
        STATE_CRAWL,
        STATE_NORMAL_STOP,
        STATE_EMERGENCY_STOP,
        STATE_WEB_BREAK,
        STATE_FAULT
    );
    END_TYPE
    MachineState : E_MachineState := STATE_INIT;

    (* Global Controls *)
    bSystemEnable           : BOOL;
    bStartCmd               : BOOL;
    bStopCmd                : BOOL;
    bEStopActive            : BOOL;
    bWebBreakDetected       : BOOL;
    bClearFaults            : BOOL;
    
    rTargetLineSpeed        : REAL;  (* Master speed setpoint (m/min) *)
    rCurrentLineSpeed       : REAL;  (* Ramped current line speed (m/min) *)
    rCrawlSpeed             : REAL := 20.0; (* m/min *)

    (* Draw Control (Cascading) Data Structures *)
    TYPE ST_DriveAxis :
    STRUCT
        Enable          : BOOL;
        Ready           : BOOL;
        Faulted         : BOOL;
        DrawSetpoint    : REAL;   (* % difference from previous section *)
        TargetSpeed     : REAL;   (* Calculated absolute target speed *)
        ActualSpeed     : REAL;   (* Feedback from encoder *)
        TorqueFeedback  : REAL;   (* Feedback for load monitoring *)
        VibrationLevel  : REAL;   (* mm/s *)
        BearingTemp     : REAL;   (* deg C *)
        ThermalOverload : BOOL;
    END_STRUCT;
    END_TYPE
    
    Axes : ARRAY[1..NUM_AXES] OF ST_DriveAxis;
    
    (* Yankee Dryer Moisture / Steam Control *)
    rIRScannerMoisture      : REAL;   (* % Moisture feedback from scanner *)
    rSteamPressureFeedback  : REAL;   (* bar *)
    rSteamValveCmd          : REAL;   (* 0-100% *)
    
    PID_Moisture : FB_PID; (* Internal PID function block instance *)
    
    (* Ramp Generator for Massive Inertia *)
    RampGen : FB_SCurveRamp;
    
    (* Indexers and Temps *)
    i : INT;
    bAnyFault : BOOL;
    rAccumulatedSpeed : REAL;
END_VAR

(* ========================================================================= *)
(* 1. SAFETY & INTERLOCKS                                                    *)
(* ========================================================================= *)
bAnyFault := FALSE;

FOR i := 1 TO NUM_AXES DO
    IF Axes[i].Faulted OR Axes[i].ThermalOverload OR (Axes[i].BearingTemp > 85.0) OR (Axes[i].VibrationLevel > 7.5) THEN
        bAnyFault := TRUE;
    END_IF;
END_FOR;

IF bEStopActive THEN
    MachineState := STATE_EMERGENCY_STOP;
ELSIF bWebBreakDetected AND MachineState = STATE_RUNNING THEN
    MachineState := STATE_WEB_BREAK;
ELSIF bAnyFault THEN
    MachineState := STATE_FAULT;
END_IF;

(* Fault Reset *)
IF bClearFaults THEN
    IF NOT bEStopActive AND NOT bAnyFault THEN
        MachineState := STATE_INIT;
    END_IF;
END_IF;

(* ========================================================================= *)
(* 2. MASTER STATE MACHINE                                                   *)
(* ========================================================================= *)
CASE MachineState OF

    STATE_INIT:
        rTargetLineSpeed := 0.0;
        rSteamValveCmd := 0.0;
        IF bSystemEnable AND NOT bEStopActive AND NOT bAnyFault THEN
            MachineState := STATE_READY;
        END_IF;

    STATE_READY:
        IF bStartCmd THEN
            rTargetLineSpeed := BASE_LINE_SPEED_MAX;
            MachineState := STATE_STARTING_RAMP;
        ELSIF bStopCmd THEN
            (* Stay ready *)
        END_IF;

    STATE_STARTING_RAMP:
        IF rCurrentLineSpeed >= (rTargetLineSpeed - 1.0) THEN
            MachineState := STATE_RUNNING;
        END_IF;
        IF bStopCmd THEN
            rTargetLineSpeed := 0.0;
            MachineState := STATE_NORMAL_STOP;
        END_IF;

    STATE_RUNNING:
        IF bStopCmd THEN
            rTargetLineSpeed := 0.0;
            MachineState := STATE_NORMAL_STOP;
        END_IF;

    STATE_NORMAL_STOP:
        IF rCurrentLineSpeed <= 1.0 THEN
            MachineState := STATE_READY;
        END_IF;

    STATE_WEB_BREAK:
        (* Rapidly decrease speed to crawl, shut off Yankee steam to prevent fire *)
        rTargetLineSpeed := rCrawlSpeed;
        rSteamValveCmd := 0.0;
        IF bStopCmd THEN
            rTargetLineSpeed := 0.0;
            MachineState := STATE_NORMAL_STOP;
        END_IF;

    STATE_EMERGENCY_STOP:
        (* Coast to stop or dynamic braking depending on VFD config; command 0 *)
        rTargetLineSpeed := 0.0;
        rCurrentLineSpeed := 0.0; (* Bypass ramp *)
        rSteamValveCmd := 0.0;

    STATE_FAULT:
        rTargetLineSpeed := 0.0;
        rSteamValveCmd := 0.0;

END_CASE;

(* ========================================================================= *)
(* 3. MASSIVE INERTIA RAMPING (S-CURVE)                                      *)
(* ========================================================================= *)
(* The immense mechanical inertia of the press and dryer rolls requires 
   extremely controlled ramping to prevent twisting and snapping the drive 
   shafts. We use an S-curve to smoothly transition accelerations. *)
   
IF MachineState <> STATE_EMERGENCY_STOP THEN
    RampGen(
        Enable := TRUE,
        TargetValue := rTargetLineSpeed,
        MaxRampRate := INERTIA_RAMP_RATE,
        SCurveTime := S_CURVE_SMOOTHING,
        CurrentValue => rCurrentLineSpeed
    );
ELSE
    RampGen(Enable := FALSE); (* Reset internal states on E-Stop *)
END_IF;

(* ========================================================================= *)
(* 4. 40-AXIS ELECTRONIC SPEED CASCADING (DRAW CONTROL)                      *)
(* ========================================================================= *)
(* To prevent tearing the wet, delicate paper web, each subsequent section 
   must run slightly faster than the previous to maintain tension. 
   Speed[n] = Speed[n-1] * (1 + Draw[n]/100) *)

rAccumulatedSpeed := rCurrentLineSpeed; (* Base speed for Axis 1 (Wire drive roll) *)

FOR i := 1 TO NUM_AXES DO
    IF i = 1 THEN
        Axes[i].TargetSpeed := rAccumulatedSpeed;
    ELSE
        (* Calculate cascading draw *)
        rAccumulatedSpeed := rAccumulatedSpeed * (1.0 + (Axes[i].DrawSetpoint / 100.0));
        Axes[i].TargetSpeed := rAccumulatedSpeed;
    END_IF;
    
    (* Enable drives based on state *)
    IF MachineState = STATE_STARTING_RAMP OR MachineState = STATE_RUNNING OR MachineState = STATE_NORMAL_STOP OR MachineState = STATE_WEB_BREAK THEN
        Axes[i].Enable := TRUE;
    ELSE
        Axes[i].Enable := FALSE;
    END_IF;
    
    (* In a real implementation, Axes[i].TargetSpeed is written out via PROFINET/EtherCAT to the VFD *)
END_FOR;

(* ========================================================================= *)
(* 5. INFRARED MOISTURE SCANNER & YANKEE DRYER STEAM CONTROL                 *)
(* ========================================================================= *)
(* The IR scanner traverses the sheet. We use its average to control the 
   Yankee dryer cylinder steam valve. A PID block maintains the setpoint. *)

IF MachineState = STATE_RUNNING THEN
    PID_Moisture(
        Enable := TRUE,
        Setpoint := MOISTURE_SETPOINT,
        ProcessVariable := rIRScannerMoisture,
        Kp := 2.5,
        Ki := 0.15,
        Kd := 0.05,
        ReverseActing := TRUE, (* Higher moisture means open valve MORE *)
        OutputMin := 0.0,
        OutputMax := STEAM_VALVE_MAX,
        Output => rSteamValveCmd
    );
ELSE
    (* Close steam valve if not running to prevent burning the paper/felt *)
    PID_Moisture(Enable := FALSE);
    rSteamValveCmd := 0.0;
END_IF;

END_PROGRAM
```"""

import sys
import os

with open(r"c:\Users\majip\Downloads\LLM REASEARCH\data\evol_instruct_dataset.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps({"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": response}]}) + "\n")
print("Written successfully")
