import json
import os

filepath = r"c:\Users\majip\Downloads\LLM REASEARCH\data\synthetic_generation_v3_enterprise.jsonl"

prompt = """Design a highly advanced PLC controller in IEC 61131-3 Structured Text for a Massive Mine Dewatering Pump Station. The station operates at a 2000-meter depth using multi-stage centrifugal pumps. The controller must include:
1. Complex sequencing for multiple 2000m-head centrifugal pumps.
2. Cascading sump level control.
3. Water-hammer prevention implementing VFD ramping and slow-opening cone valves."""

response = """(* 
================================================================================
ENTERPRISE-GRADE MINE DEWATERING PUMP STATION CONTROLLER
================================================================================
Target Platform: Siemens S7-1500 / Allen-Bradley ControlLogix
Language: IEC 61131-3 Structured Text (ST)
Revision: 4.1.0
Author: Lumina Elite Synthetic Data Architect
Description:
Massive deep-mine dewatering system handling 2000m head using 4 multi-stage 
centrifugal pumps. Features dynamic cascading sump level control, VFD ramping, 
slow-opening cone valve sequencing for severe water-hammer prevention, and 
equipment wear-leveling (duty/standby rotation).
================================================================================
*)

TYPE
    E_PumpState : (
        STATE_OFF := 0,
        STATE_VFD_RAMP_UP := 1,
        STATE_CONE_VALVE_OPENING := 2,
        STATE_RUNNING := 3,
        STATE_CONE_VALVE_CLOSING := 4,
        STATE_VFD_RAMP_DOWN := 5,
        STATE_FAULT := 99
    );
    
    T_PumpConfig : STRUCT
        ID : INT;
        IsDuty : BOOL;
        RunTimeHours : REAL;
        StartsCount : DINT;
        Enabled : BOOL;
    END_STRUCT;
    
    T_PumpAnalog : STRUCT
        SpeedSetpoint : REAL;
        SpeedFeedback : REAL;
        ConeValvePos : REAL;  (* 0.0 to 100.0% *)
        MotorTemp : REAL;
        BearingTemp : REAL;
        VibrationDrive : REAL;
        VibrationNonDrive : REAL;
    END_STRUCT;
END_TYPE

FUNCTION_BLOCK FB_DeepMineDewatering
VAR_INPUT
    EnableSystem : BOOL;
    EmergencyStop : BOOL;
    SumpLevel_m : REAL;
    PressureHeader_bar : REAL;
    FlowRateHeader_m3h : REAL;
    
    ResetFaults : BOOL;
END_VAR

VAR_OUTPUT
    SystemReady : BOOL;
    ActivePumpsCount : INT;
    HeaderPressureWarning : BOOL;
    SystemFault : BOOL;
END_VAR

VAR
    // Configurations
    MAX_PUMPS : INT := 4;
    LEVEL_LL : REAL := 2.0; (* Trip level *)
    LEVEL_L  : REAL := 4.0; (* Stop pumps *)
    LEVEL_H  : REAL := 8.0; (* Start 1st pump *)
    LEVEL_HH : REAL := 12.0; (* Start 2nd pump *)
    LEVEL_HHH: REAL := 15.0; (* Start 3rd pump *)
    LEVEL_MAX: REAL := 18.0; (* Overflow alarm *)
    
    // Pump Data
    PumpsCfg : ARRAY[1..4] OF T_PumpConfig;
    PumpsState : ARRAY[1..4] OF E_PumpState;
    PumpsData : ARRAY[1..4] OF T_PumpAnalog;
    PumpsFault : ARRAY[1..4] OF BOOL;
    
    // Command Outputs
    CmdVFDRun : ARRAY[1..4] OF BOOL;
    CmdVFDSpeedRef : ARRAY[1..4] OF REAL;
    CmdValveOpen : ARRAY[1..4] OF BOOL;
    CmdValveClose : ARRAY[1..4] OF BOOL;
    
    // Timers & Triggers
    TmrDutyRotate : TON;
    TmrPumpSequencer : TON;
    TmrValveTrans : ARRAY[1..4] OF TON;
    TmrVFDRamp : ARRAY[1..4] OF TON;
    
    RequiredPumps : INT := 0;
    i : INT;
    j : INT;
    TempID : INT;
    TempTime : REAL;
    
    SortedPumpIdx : ARRAY[1..4] OF INT;
    
    // PID for Cascading Control
    LevelPID_Kp : REAL := 2.5;
    LevelPID_Ki : REAL := 0.1;
    LevelPID_Error : REAL;
    LevelPID_Integral : REAL;
    SpeedRequest : REAL;
    
    // Water Hammer Constraints
    RAMP_UP_TIME_S : TIME := T#180s;
    RAMP_DOWN_TIME_S : TIME := T#240s;
    VALVE_OPEN_TIME_S : TIME := T#300s; // 5 min cone valve open
    VALVE_CLOSE_TIME_S : TIME := T#300s;
END_VAR

(* ==============================================================================
   1. SYSTEM SAFETY & INITIALIZATION
============================================================================== *)
IF EmergencyStop OR (SumpLevel_m <= LEVEL_LL) THEN
    // Immediate shutdown bypassing water hammer protection
    FOR i := 1 TO MAX_PUMPS DO
        CmdVFDRun[i] := FALSE;
        CmdVFDSpeedRef[i] := 0.0;
        CmdValveOpen[i] := FALSE;
        CmdValveClose[i] := TRUE;
        IF PumpsState[i] <> STATE_OFF THEN
            PumpsState[i] := STATE_FAULT;
            PumpsFault[i] := TRUE;
        END_IF;
    END_FOR;
    SystemFault := TRUE;
    ActivePumpsCount := 0;
    RETURN;
END_IF;

IF ResetFaults THEN
    SystemFault := FALSE;
    FOR i := 1 TO MAX_PUMPS DO
        PumpsFault[i] := FALSE;
        IF PumpsState[i] = STATE_FAULT THEN
            PumpsState[i] := STATE_OFF;
        END_IF;
    END_FOR;
END_IF;

SystemReady := EnableSystem AND NOT SystemFault;

(* ==============================================================================
   2. CASCADING SUMP LEVEL CONTROL (DEMAND DETERMINATION)
============================================================================== *)
IF SystemReady THEN
    IF SumpLevel_m > LEVEL_HHH THEN
        RequiredPumps := 3;
    ELSIF SumpLevel_m > LEVEL_HH THEN
        RequiredPumps := 2;
    ELSIF SumpLevel_m > LEVEL_H THEN
        RequiredPumps := 1;
    ELSIF SumpLevel_m < LEVEL_L THEN
        RequiredPumps := 0;
    END_IF;
ELSE
    RequiredPumps := 0;
END_IF;

(* PID calculation for VFD speed fine-tuning based on level *)
LevelPID_Error := SumpLevel_m - LEVEL_L;
IF LevelPID_Error > 0.0 AND SystemReady THEN
    LevelPID_Integral := LevelPID_Integral + (LevelPID_Error * 0.1); // Assuming 100ms task
ELSE
    LevelPID_Integral := 0.0;
END_IF;

SpeedRequest := (LevelPID_Error * LevelPID_Kp) + (LevelPID_Integral * LevelPID_Ki);
IF SpeedRequest > 100.0 THEN SpeedRequest := 100.0; END_IF;
IF SpeedRequest < 60.0 THEN SpeedRequest := 60.0; END_IF; // Min speed for 2000m head to overcome check valve

(* ==============================================================================
   3. WEAR-LEVELING / DUTY STANDBY ROTATION
============================================================================== *)
// Initialize indices
FOR i := 1 TO MAX_PUMPS DO
    SortedPumpIdx[i] := i;
END_FOR;

// Sort by RunTime (Bubble sort for simplicity on 4 items)
FOR i := 1 TO MAX_PUMPS - 1 DO
    FOR j := i + 1 TO MAX_PUMPS DO
        IF PumpsCfg[SortedPumpIdx[i]].RunTimeHours > PumpsCfg[SortedPumpIdx[j]].RunTimeHours THEN
            TempID := SortedPumpIdx[i];
            SortedPumpIdx[i] := SortedPumpIdx[j];
            SortedPumpIdx[j] := TempID;
        END_IF;
    END_FOR;
END_FOR;

(* ==============================================================================
   4. PUMP SEQUENCING & WATER-HAMMER PREVENTION STATE MACHINE
============================================================================== *)
ActivePumpsCount := 0;

FOR i := 1 TO MAX_PUMPS DO
    TempID := SortedPumpIdx[i];
    
    // Determine if this pump should be running based on RequiredPumps
    PumpsCfg[TempID].IsDuty := (i <= RequiredPumps) AND PumpsCfg[TempID].Enabled AND NOT PumpsFault[TempID];
    
    CASE PumpsState[TempID] OF
        
        STATE_OFF:
            CmdVFDRun[TempID] := FALSE;
            CmdVFDSpeedRef[TempID] := 0.0;
            CmdValveOpen[TempID] := FALSE;
            CmdValveClose[TempID] := TRUE;
            
            IF PumpsCfg[TempID].IsDuty THEN
                PumpsState[TempID] := STATE_VFD_RAMP_UP;
                PumpsCfg[TempID].StartsCount := PumpsCfg[TempID].StartsCount + 1;
            END_IF;
            
        STATE_VFD_RAMP_UP:
            CmdVFDRun[TempID] := TRUE;
            CmdVFDSpeedRef[TempID] := 100.0; // Target full speed for starting against closed cone valve
            
            // Wait for VFD to reach operating speed before opening valve
            IF PumpsData[TempID].SpeedFeedback >= 98.0 THEN
                PumpsState[TempID] := STATE_CONE_VALVE_OPENING;
            END_IF;
            
            IF NOT PumpsCfg[TempID].IsDuty THEN
                PumpsState[TempID] := STATE_VFD_RAMP_DOWN;
            END_IF;
            
        STATE_CONE_VALVE_OPENING:
            // Slowly open cone valve to prevent water hammer
            CmdValveOpen[TempID] := TRUE;
            CmdValveClose[TempID] := FALSE;
            
            IF PumpsData[TempID].ConeValvePos >= 98.0 THEN
                PumpsState[TempID] := STATE_RUNNING;
            END_IF;
            
            IF NOT PumpsCfg[TempID].IsDuty THEN
                PumpsState[TempID] := STATE_CONE_VALVE_CLOSING;
            END_IF;
            
        STATE_RUNNING:
            ActivePumpsCount := ActivePumpsCount + 1;
            CmdValveOpen[TempID] := TRUE;
            CmdValveClose[TempID] := FALSE;
            
            // Modulate speed based on PID
            CmdVFDSpeedRef[TempID] := SpeedRequest;
            
            IF NOT PumpsCfg[TempID].IsDuty THEN
                PumpsState[TempID] := STATE_CONE_VALVE_CLOSING;
            END_IF;
            
        STATE_CONE_VALVE_CLOSING:
            // Maintain VFD speed while closing cone valve slowly
            CmdVFDSpeedRef[TempID] := 100.0; 
            CmdValveOpen[TempID] := FALSE;
            CmdValveClose[TempID] := TRUE;
            
            IF PumpsData[TempID].ConeValvePos <= 2.0 THEN
                PumpsState[TempID] := STATE_VFD_RAMP_DOWN;
            END_IF;
            
            IF PumpsCfg[TempID].IsDuty THEN
                PumpsState[TempID] := STATE_CONE_VALVE_OPENING;
            END_IF;
            
        STATE_VFD_RAMP_DOWN:
            CmdVFDRun[TempID] := FALSE; // Let VFD handle ramp down
            CmdVFDSpeedRef[TempID] := 0.0;
            
            IF PumpsData[TempID].SpeedFeedback <= 2.0 THEN
                PumpsState[TempID] := STATE_OFF;
            END_IF;
            
        STATE_FAULT:
            CmdVFDRun[TempID] := FALSE;
            CmdVFDSpeedRef[TempID] := 0.0;
            CmdValveOpen[TempID] := FALSE;
            CmdValveClose[TempID] := TRUE; // Fail safe closed
            
    END_CASE;
    
    // Vibration & Temp Monitoring (Fault Triggers)
    IF PumpsData[TempID].BearingTemp > 90.0 OR 
       PumpsData[TempID].MotorTemp > 130.0 OR 
       PumpsData[TempID].VibrationDrive > 8.0 THEN
        PumpsState[TempID] := STATE_FAULT;
        PumpsFault[TempID] := TRUE;
    END_IF;
    
END_FOR;

HeaderPressureWarning := (PressureHeader_bar > 250.0); // 2000m ~ 200 bar

END_FUNCTION_BLOCK
"""

entry = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": response}
    ]
}

with open(filepath, "a", encoding="utf-8") as f:
    f.write(json.dumps(entry) + "\n")

print("Appended successfully.")
