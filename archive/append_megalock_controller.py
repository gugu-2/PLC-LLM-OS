import json

data = {
    "messages": [
        {
            "role": "user",
            "content": "You are acting as a Lead Civil Engineer. Evolve a basic sequencer into a Panama Canal Mega-Lock Gate Controller. Technical Specs: 1. 3,000-ton rolling gate dual-drive synchronization. 2. Culvert filling/emptying valve sequencing to prevent turbulent currents from snapping mooring lines. 3. Seawater/Freshwater salinity density tracking matrices. Append to synthetic_generation_v3_enterprise.jsonl."
        },
        {
            "role": "assistant",
            "content": """```pascal
(*
================================================================================
Panama Canal Mega-Lock Gate Controller (Neopanamax Class)
================================================================================
Description:
Highly complex IEC 61131-3 implementation for managing the critical operations
of a 3,000-ton rolling gate, integrating dual-drive synchronization, culvert 
filling/emptying valve sequencing for anti-turbulence, and seawater/freshwater
salinity density matrices.

Features:
- Dual-Drive Synchronization (Master/Slave Cross-Coupled PID)
- Culvert Valve Flow Control (Multi-stage sequencing, anti-turbulence)
- Hydrological Salinity/Density Tracking Matrices
- Comprehensive State Machine and Alarming
================================================================================
*)

TYPE
    ST_Drive_Status : STRUCT
        Position     : LREAL; (* mm *)
        Velocity     : LREAL; (* mm/s *)
        Torque       : LREAL; (* kNm *)
        Is_Healthy   : BOOL;
        Overload     : BOOL;
        Brake_Status : BOOL;
    END_STRUCT;
    
    ST_Hydrology_Data : STRUCT
        Level        : LREAL; (* m *)
        Salinity     : LREAL; (* PSU *)
        Temperature  : LREAL; (* Celsius *)
        Density      : LREAL; (* kg/m^3 computed *)
    END_STRUCT;
    
    ST_Culvert_Valves : STRUCT
        Target_Pos   : ARRAY[1..4] OF LREAL; (* 0..100% *)
        Actual_Pos   : ARRAY[1..4] OF LREAL;
        Is_Moving    : ARRAY[1..4] OF BOOL;
    END_STRUCT;
END_TYPE

FUNCTION Calculate_Density : LREAL
VAR_INPUT
    Salinity : LREAL; (* PSU *)
    Temp     : LREAL; (* Deg C *)
END_VAR
VAR
    A, B, C : LREAL;
    Rho_0 : LREAL;
END_VAR
    (* UNESCO Equation of State for Seawater (Simplified) *)
    Rho_0 := 999.842594 + (6.793952E-2 * Temp) - (9.095290E-3 * EXPT(Temp, 2)) + (1.001685E-4 * EXPT(Temp, 3));
    A := 8.24493E-1 - (4.0899E-3 * Temp) + (7.6438E-5 * EXPT(Temp, 2));
    B := -5.72466E-3 + (1.0227E-4 * Temp);
    C := 4.8314E-4;
    
    Calculate_Density := Rho_0 + A * Salinity + B * EXPT(Salinity, 1.5) + C * EXPT(Salinity, 2);
END_FUNCTION

FUNCTION_BLOCK FB_DualDrive_Sync
VAR_INPUT
    Enable        : BOOL;
    Target_Pos    : LREAL;
    Target_Vel    : LREAL;
    Drive1        : ST_Drive_Status;
    Drive2        : ST_Drive_Status;
    Kp            : LREAL := 2.5;
    Ki            : LREAL := 0.15;
    Kd            : LREAL := 0.05;
    Max_Correction: LREAL := 15.0; (* mm/s *)
    Cycle_Time    : LREAL := 0.01; (* s *)
END_VAR
VAR_OUTPUT
    Cmd_Vel_D1    : LREAL;
    Cmd_Vel_D2    : LREAL;
    Cmd_Trq_Lim_D1: LREAL;
    Cmd_Trq_Lim_D2: LREAL;
    Sync_Error    : LREAL;
    Alarm_Desync  : BOOL;
END_VAR
VAR
    Prev_Error    : LREAL;
    Integral      : LREAL;
    Derivative    : LREAL;
    Correction    : LREAL;
END_VAR
    IF NOT Enable THEN
        Cmd_Vel_D1 := 0.0;
        Cmd_Vel_D2 := 0.0;
        Integral := 0.0;
        Alarm_Desync := FALSE;
        RETURN;
    END_IF;
    
    Sync_Error := Drive1.Position - Drive2.Position;
    
    IF ABS(Sync_Error) > 50.0 THEN (* 50 mm max deviation *)
        Alarm_Desync := TRUE;
    ELSE
        Alarm_Desync := FALSE;
    END_IF;
    
    Integral := Integral + (Sync_Error * Cycle_Time);
    Integral := LIMIT(-Max_Correction/Ki, Integral, Max_Correction/Ki);
    Derivative := (Sync_Error - Prev_Error) / Cycle_Time;
    Prev_Error := Sync_Error;
    
    Correction := (Kp * Sync_Error) + (Ki * Integral) + (Kd * Derivative);
    Correction := LIMIT(-Max_Correction, Correction, Max_Correction);
    
    (* Master/Slave Velocity distribution *)
    Cmd_Vel_D1 := Target_Vel - (Correction / 2.0);
    Cmd_Vel_D2 := Target_Vel + (Correction / 2.0);
    
    (* 3,000-ton torque management (1500 ton per drive equivalent) *)
    Cmd_Trq_Lim_D1 := 8500.0; (* kNm base limit *)
    Cmd_Trq_Lim_D2 := 8500.0;
END_FUNCTION_BLOCK

FUNCTION_BLOCK FB_MegaLock_Controller
VAR_INPUT
    (* Commands *)
    Cmd_Initiate_Transit : BOOL;
    Cmd_Emergency_Stop   : BOOL;
    Transit_Direction    : INT; (* 1 = Ocean to Lake, -1 = Lake to Ocean *)
    
    (* Hydrology Sensors *)
    Sensor_Ocean         : ST_Hydrology_Data;
    Sensor_Lake          : ST_Hydrology_Data;
    Sensor_Chamber       : ST_Hydrology_Data;
    
    (* Gate Drives *)
    Gate_D1              : ST_Drive_Status;
    Gate_D2              : ST_Drive_Status;
    
    (* System Cycle Time *)
    CycleTime            : LREAL := 0.01;
END_VAR

VAR_OUTPUT
    (* Drive Commands *)
    Out_Gate_Vel_Cmd_D1  : LREAL;
    Out_Gate_Vel_Cmd_D2  : LREAL;
    Out_Gate_Trq_Lim_D1  : LREAL;
    Out_Gate_Trq_Lim_D2  : LREAL;
    Out_Gate_Brake_Rel   : BOOL;
    
    (* Culvert Valves *)
    Out_Fill_Valves      : ST_Culvert_Valves;
    Out_Empty_Valves     : ST_Culvert_Valves;
    
    (* State & Diagnostics *)
    Current_State        : STRING(50);
    Alarm_Turbulence     : BOOL;
    Alarm_Sync           : BOOL;
    Alarm_Density_Diff   : BOOL;
END_VAR

VAR
    (* Internal Instances *)
    fbSyncCtrl           : FB_DualDrive_Sync;
    
    (* State Machine *)
    Step                 : INT := 0;
    Timer                : LREAL := 0.0;
    
    (* Matrices & Hydrology Calculations *)
    Density_Matrix       : ARRAY[1..3, 1..3] OF LREAL; (* Tracking across levels/chambers *)
    Differential_Head    : LREAL;
    Max_Flow_Rate        : LREAL;
    Target_Valve_Opening : LREAL;
    i                    : INT;
    
    Gate_Target_Pos      : LREAL;
    Gate_Target_Vel      : LREAL;
END_VAR

    (* Update Hydrology Matrices *)
    Sensor_Ocean.Density := Calculate_Density(Sensor_Ocean.Salinity, Sensor_Ocean.Temperature);
    Sensor_Lake.Density := Calculate_Density(Sensor_Lake.Salinity, Sensor_Lake.Temperature);
    Sensor_Chamber.Density := Calculate_Density(Sensor_Chamber.Salinity, Sensor_Chamber.Temperature);
    
    (* 3x3 Matrix for gradient mapping - simplified representation *)
    Density_Matrix[1,1] := Sensor_Ocean.Density;
    Density_Matrix[2,2] := Sensor_Chamber.Density;
    Density_Matrix[3,3] := Sensor_Lake.Density;
    
    IF ABS(Sensor_Ocean.Density - Sensor_Chamber.Density) > 25.0 THEN
        Alarm_Density_Diff := TRUE; (* Significant halocline detected, adjusting flow rate *)
    ELSE
        Alarm_Density_Diff := FALSE;
    END_IF;

    (* Emergency Stop Override *)
    IF Cmd_Emergency_Stop THEN
        Step := 999;
    END_IF;

    (* Main State Machine *)
    CASE Step OF
        0: (* IDLE *)
            Current_State := 'IDLE';
            Out_Gate_Brake_Rel := FALSE;
            Gate_Target_Vel := 0.0;
            FOR i := 1 TO 4 DO
                Out_Fill_Valves.Target_Pos[i] := 0.0;
                Out_Empty_Valves.Target_Pos[i] := 0.0;
            END_FOR;
            
            IF Cmd_Initiate_Transit THEN
                Step := 10;
                Timer := 0.0;
            END_IF;
            
        10: (* ANALYZE HYDRAULIC HEAD & SALINITY *)
            Current_State := 'CALCULATING_FLOW_DYNAMICS';
            IF Transit_Direction = 1 THEN
                Differential_Head := Sensor_Lake.Level - Sensor_Chamber.Level;
            ELSE
                Differential_Head := Sensor_Chamber.Level - Sensor_Ocean.Level;
            END_IF;
            
            (* Prevent snapping mooring lines: Limit initial flow rate based on head and density diff *)
            Max_Flow_Rate := 120.0 - (ABS(Differential_Head) * 2.0); (* m^3/s limit *)
            IF Alarm_Density_Diff THEN
                Max_Flow_Rate := Max_Flow_Rate * 0.7; (* Reduce flow by 30% to prevent turbulent density currents *)
            END_IF;
            
            Target_Valve_Opening := (Max_Flow_Rate / 250.0) * 100.0; (* Linearized valve approximation *)
            Step := 20;
            
        20: (* VALVE SEQUENCING - FILL/EMPTY *)
            Current_State := 'VALVE_SEQUENCING';
            Timer := Timer + CycleTime;
            
            (* Open valves symmetrically and staged to minimize turbulence *)
            IF Timer < 60.0 THEN
                (* Stage 1: Crack open inner valves (2 and 3) *)
                Out_Fill_Valves.Target_Pos[2] := Target_Valve_Opening * 0.25;
                Out_Fill_Valves.Target_Pos[3] := Target_Valve_Opening * 0.25;
            ELSIF Timer < 180.0 THEN
                (* Stage 2: Gradually open outer valves *)
                Out_Fill_Valves.Target_Pos[1] := Target_Valve_Opening * 0.5;
                Out_Fill_Valves.Target_Pos[4] := Target_Valve_Opening * 0.5;
                Out_Fill_Valves.Target_Pos[2] := Target_Valve_Opening * 0.5;
                Out_Fill_Valves.Target_Pos[3] := Target_Valve_Opening * 0.5;
            ELSIF Differential_Head < 0.1 THEN
                (* Levels equalized *)
                Step := 30;
                Timer := 0.0;
            END_IF;
            
        30: (* CLOSE VALVES *)
            Current_State := 'CLOSING_VALVES';
            FOR i := 1 TO 4 DO
                Out_Fill_Valves.Target_Pos[i] := 0.0;
            END_FOR;
            Step := 40;
            
        40: (* OPEN 3000-TON ROLLING GATE *)
            Current_State := 'GATE_OPENING_SYNC';
            Out_Gate_Brake_Rel := TRUE;
            Gate_Target_Pos := 35000.0; (* 35 meters open *)
            
            (* Ramp up velocity *)
            IF Gate_Target_Vel < 150.0 THEN
                Gate_Target_Vel := Gate_Target_Vel + (5.0 * CycleTime); (* mm/s^2 accel *)
            END_IF;
            
            IF (Gate_D1.Position > 34950.0) AND (Gate_D2.Position > 34950.0) THEN
                Gate_Target_Vel := 0.0;
                Step := 50;
            END_IF;
            
        50: (* TRANSIT COMPLETE *)
            Current_State := 'TRANSIT_COMPLETE_HOLD';
            Out_Gate_Brake_Rel := FALSE;
            IF NOT Cmd_Initiate_Transit THEN
                Step := 0;
            END_IF;
            
        999: (* EMERGENCY STOP *)
            Current_State := 'EMERGENCY_STOP';
            Out_Gate_Brake_Rel := FALSE;
            Gate_Target_Vel := 0.0;
            FOR i := 1 TO 4 DO
                Out_Fill_Valves.Target_Pos[i] := 0.0;
                Out_Empty_Valves.Target_Pos[i] := 0.0;
            END_FOR;
            IF NOT Cmd_Emergency_Stop THEN
                Step := 0;
            END_IF;
    END_CASE;
    
    (* Execute Dual-Drive Sync Control *)
    fbSyncCtrl(
        Enable := (Step = 40) OR (Step = 60),
        Target_Pos := Gate_Target_Pos,
        Target_Vel := Gate_Target_Vel,
        Drive1 := Gate_D1,
        Drive2 := Gate_D2,
        Cycle_Time := CycleTime,
        Cmd_Vel_D1 => Out_Gate_Vel_Cmd_D1,
        Cmd_Vel_D2 => Out_Gate_Vel_Cmd_D2,
        Cmd_Trq_Lim_D1 => Out_Gate_Trq_Lim_D1,
        Cmd_Trq_Lim_D2 => Out_Gate_Trq_Lim_D2,
        Alarm_Desync => Alarm_Sync
    );
    
END_FUNCTION_BLOCK
```"""
        }
    ]
}

target_file = r'c:\Users\majip\Downloads\LLM REASEARCH\data\synthetic_generation_v3_enterprise.jsonl'
with open(target_file, 'a', encoding='utf-8') as f:
    f.write(json.dumps(data) + '\n')
