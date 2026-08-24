import json

system_prompt = "You are acting as a Lead Show Engineer for a mega-casino. Evolve a basic timer into a Massive Choreographed Fountain Controller (e.g., Bellagio). Technical Specs: 1. Oarsman nozzle 2-axis servo tracking synchronized to audio SMPTE timecode. 2. Variable frequency drive (VFD) pressure matrices for 400-foot water shooters. 3. Wind speed anemometer safety dampening. Append to synthetic_generation_v3_enterprise.jsonl."

assistant_response = '''(*
================================================================================
BELLAGIO-CLASS MASSIVE CHOREOGRAPHED FOUNTAIN CONTROLLER
================================================================================
System Architecture: Mega-Casino Show Engineering
Module: FB_Mega_Fountain_Controller
Language: IEC 61131-3 Structured Text (ST)
Author: Lead Show Engineer

DESCRIPTION:
Evolves a primitive time-based driver into a full-scale hydrodynamic show matrix.
Integrates SMPTE timecode synchronization for precise Oarsman 2-axis servo tracking,
VFD (Variable Frequency Drive) pressure matrices for 400ft super-shooters, and 
real-time anemometer-based safety dampening to prevent unintended guest soaking.
================================================================================
*)

TYPE ST_SMPTE_Time :
STRUCT
    Hours   : USINT;
    Minutes : USINT;
    Seconds : USINT;
    Frames  : USINT;
END_STRUCT
END_TYPE

TYPE ST_Oarsman_Nozzle :
STRUCT
    Pan_Target_Deg  : REAL; (* -180.0 to 180.0 *)
    Tilt_Target_Deg : REAL; (* 0.0 to 90.0 *)
    Current_Pan     : REAL;
    Current_Tilt    : REAL;
    Servo_Enable    : BOOL;
    Fault_Active    : BOOL;
END_STRUCT
END_TYPE

TYPE ST_VFD_Pump :
STRUCT
    Speed_Setpoint_Pct : REAL; (* 0.0 to 100.0% *)
    Current_Speed_Pct  : REAL;
    Run_Command        : BOOL;
    Fault              : BOOL;
END_STRUCT
END_TYPE

TYPE ST_Anemometer_Data :
STRUCT
    Wind_Speed_MPH  : REAL;
    Wind_Dir_Deg    : REAL;
    Gust_Peak_MPH   : REAL;
END_STRUCT
END_TYPE

FUNCTION_BLOCK FB_Mega_Fountain_Controller
VAR_INPUT
    Enable_Show         : BOOL;
    SMPTE_Input         : ST_SMPTE_Time;
    Anemometer          : ST_Anemometer_Data;
    Emergency_Stop      : BOOL;
END_VAR

VAR_OUTPUT
    System_Ready        : BOOL;
    Show_Running        : BOOL;
    Wind_Dampening_Pct  : REAL;
    Safety_Abort        : BOOL;
END_VAR

VAR_IN_OUT
    Oarsman_Matrix      : ARRAY[1..120] OF ST_Oarsman_Nozzle;
    Extreme_Shooter_VFD : ARRAY[1..40] OF ST_VFD_Pump;
END_VAR

VAR
    Show_Timer          : TON;
    Current_Total_Frames: UDINT;
    i                   : INT;
    Wind_Limit_Warning  : REAL := 15.0; (* MPH *)
    Wind_Limit_Abort    : REAL := 25.0; (* MPH *)
    Safety_Dampening    : REAL := 1.0;  (* 1.0 = 100% output, 0.0 = Off *)
    
    (* Choreography Memory Pointers (Simplified for ST representation) *)
    Pan_Choreo_Table    : ARRAY[0..36000] OF REAL; (* Indexed by Total Frames *)
    Tilt_Choreo_Table   : ARRAY[0..36000] OF REAL;
    Shooter_Choreo_Table: ARRAY[0..36000] OF REAL;
END_VAR

(*----------------------------------------------------------------------------
  1. SAFETY AND WIND DAMPENING MATRIX
-----------------------------------------------------------------------------*)
IF Emergency_Stop OR (Anemometer.Wind_Speed_MPH > Wind_Limit_Abort) THEN
    Safety_Abort := TRUE;
    Show_Running := FALSE;
    Safety_Dampening := 0.0;
ELSIF Anemometer.Wind_Speed_MPH > Wind_Limit_Warning THEN
    (* Linear dampening between Warning (15MPH) and Abort (25MPH) *)
    Safety_Dampening := 1.0 - ((Anemometer.Wind_Speed_MPH - Wind_Limit_Warning) / (Wind_Limit_Abort - Wind_Limit_Warning));
    Safety_Abort := FALSE;
ELSE
    Safety_Dampening := 1.0;
    Safety_Abort := FALSE;
END_IF

Wind_Dampening_Pct := Safety_Dampening * 100.0;

(*----------------------------------------------------------------------------
  2. SMPTE TIMECODE TRANSLATION
-----------------------------------------------------------------------------*)
(* Assuming 30 frames per second standard *)
Current_Total_Frames := (UDINT#30 * 60 * 60 * SMPTE_Input.Hours) +
                        (UDINT#30 * 60 * SMPTE_Input.Minutes) +
                        (UDINT#30 * SMPTE_Input.Seconds) +
                        SMPTE_Input.Frames;

(*----------------------------------------------------------------------------
  3. SYSTEM STATE MACHINE & EXECUTION
-----------------------------------------------------------------------------*)
IF Enable_Show AND NOT Safety_Abort THEN
    System_Ready := TRUE;
    Show_Running := TRUE;
    
    (* Protect against table out-of-bounds *)
    IF Current_Total_Frames > UDINT#36000 THEN
        Current_Total_Frames := UDINT#36000;
    END_IF
    
    (* A. OARSMAN NOZZLE 2-AXIS KINEMATICS MATRIX (120 Units) *)
    FOR i := 1 TO 120 DO
        IF NOT Oarsman_Matrix[i].Fault_Active THEN
            Oarsman_Matrix[i].Servo_Enable := TRUE;
            
            (* Apply choreographed waypoints with spatial offset algorithms based on nozzle index *)
            (* Real system interpolates between keyframes; here we read synchronized frame data *)
            Oarsman_Matrix[i].Pan_Target_Deg  := Pan_Choreo_Table[Current_Total_Frames] + (INT_TO_REAL(i) * 0.5);
            Oarsman_Matrix[i].Tilt_Target_Deg := Tilt_Choreo_Table[Current_Total_Frames];
            
            (* Wind Compensation: Angle down slightly in high winds *)
            IF Safety_Dampening < 1.0 THEN
                Oarsman_Matrix[i].Tilt_Target_Deg := Oarsman_Matrix[i].Tilt_Target_Deg * Safety_Dampening;
            END_IF
        ELSE
            Oarsman_Matrix[i].Servo_Enable := FALSE;
        END_IF
    END_FOR

    (* B. 400-FOOT EXTREME SHOOTER VFD CONTROL (40 Units) *)
    FOR i := 1 TO 40 DO
        IF NOT Extreme_Shooter_VFD[i].Fault THEN
            Extreme_Shooter_VFD[i].Run_Command := TRUE;
            
            (* Fetch base choreo speed and apply dynamic environmental dampening *)
            Extreme_Shooter_VFD[i].Speed_Setpoint_Pct := Shooter_Choreo_Table[Current_Total_Frames] * Safety_Dampening;
            
            (* Deadband for VFD stability *)
            IF Extreme_Shooter_VFD[i].Speed_Setpoint_Pct < 5.0 THEN
                Extreme_Shooter_VFD[i].Speed_Setpoint_Pct := 0.0;
                Extreme_Shooter_VFD[i].Run_Command := FALSE;
            END_IF
        ELSE
            Extreme_Shooter_VFD[i].Run_Command := FALSE;
            Extreme_Shooter_VFD[i].Speed_Setpoint_Pct := 0.0;
        END_IF
    END_FOR

ELSE
    (* ABORT / IDLE STATE: Safe shutdown of all hydrodynamic actuators *)
    System_Ready := NOT Safety_Abort;
    Show_Running := FALSE;
    
    FOR i := 1 TO 120 DO
        Oarsman_Matrix[i].Servo_Enable := FALSE;
        Oarsman_Matrix[i].Pan_Target_Deg := 0.0;
        Oarsman_Matrix[i].Tilt_Target_Deg := 0.0;
    END_FOR
    
    FOR i := 1 TO 40 DO
        Extreme_Shooter_VFD[i].Run_Command := FALSE;
        Extreme_Shooter_VFD[i].Speed_Setpoint_Pct := 0.0;
    END_FOR
END_IF
'''

data = {
    "messages": [
        {"role": "user", "content": system_prompt},
        {"role": "assistant", "content": assistant_response}
    ]
}

with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(data) + "\\n")
