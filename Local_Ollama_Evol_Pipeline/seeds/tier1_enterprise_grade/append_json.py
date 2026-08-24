import json
import os

file_path = r"c:\Users\majip\Downloads\LLM REASEARCH\Local_Ollama_Evol_Pipeline\seeds\tier1_enterprise_grade\synthetic_generation_v3_enterprise.jsonl"

user_content = "You are acting as a Lead Structural Engineer. Evolve a basic motion block into a Taipei 101 Tuned Mass Damper (TMD) Active Control System. Technical Specs: 1. 700-ton steel pendulum active hydraulic dampening. 2. Seismic P-wave early warning network integration. 3. Typhoon sustained wind-load displacement matrices. Append to synthetic_generation_v3_enterprise.jsonl."

assistant_content = """```iecst
(*
================================================================================
Taipei 101 Tuned Mass Damper (TMD) Active Control System
Version: 3.0.0 (Enterprise-Grade Structural Control)
Lead Structural Engineer / Control Systems Architect
================================================================================

Technical Specs Implemented:
1. 700-ton steel pendulum active hydraulic dampening control.
2. Seismic P-wave early warning network integration (high-priority interrupt).
3. Typhoon sustained wind-load displacement matrices (active compensation).

System Overview:
This function block manages the active and semi-active damping of the 700-ton
TMD. It incorporates early warning seismic data to precondition the hydraulic
actuators, and utilizes wind-load displacement matrices for sustained typhoon
buffeting compensation.
*)

TYPE
    T_SeismicData : STRUCT
        P_Wave_Detected : BOOL;
        Estimated_Magnitude : REAL; (* Richter *)
        Time_To_S_Wave : TIME;
        Epicenter_Distance : REAL; (* km *)
        Peak_Ground_Accel : REAL; (* g *)
    END_STRUCT;

    T_WindData : STRUCT
        Sustained_Speed : REAL; (* m/s *)
        Gust_Speed : REAL; (* m/s *)
        Direction : REAL; (* Degrees 0-359 *)
        Barometric_Pressure : REAL; (* hPa *)
    END_STRUCT;

    T_PendulumState : STRUCT
        Disp_X : REAL; (* meters *)
        Disp_Y : REAL; (* meters *)
        Vel_X : REAL; (* m/s *)
        Vel_Y : REAL; (* m/s *)
        Phase_Angle : REAL; (* rad *)
        Cable_Tension : ARRAY[1..8] OF REAL; (* kN *)
    END_STRUCT;

    T_HydraulicCommand : STRUCT
        Actuator_Force_X : REAL; (* kN *)
        Actuator_Force_Y : REAL; (* kN *)
        Valve_Open_X : REAL; (* 0-100% *)
        Valve_Open_Y : REAL; (* 0-100% *)
        Lock_Engaged : BOOL;
    END_STRUCT;
END_TYPE

FUNCTION_BLOCK FB_Taipei101_TMD_ActiveControl
VAR_INPUT
    Enable : BOOL;
    Emergency_Stop : BOOL;
    
    // Sensor Networks
    Seismic_Network : T_SeismicData;
    Anemometer_Array : T_WindData;
    Pendulum_Sensors : T_PendulumState;
    Bldg_Accel_X : REAL;
    Bldg_Accel_Y : REAL;
    
    // Hydraulic System Status
    Hyd_Pressure : REAL; (* Bar *)
    Oil_Temp : REAL; (* Celcius *)
END_VAR

VAR_OUTPUT
    Hyd_Command : T_HydraulicCommand;
    System_Status : STRING[50];
    Fault_Code : DWORD;
    Ready_For_Seismic : BOOL;
    Typhoon_Mode_Active : BOOL;
END_VAR

VAR
    // Internal States
    State : INT := 0; 
    Filter_X, Filter_Y : LREAL;
    
    // PID/State-Space Controllers
    Kp_Wind, Kd_Wind : REAL := 1500.0;
    Kp_Seismic, Kd_Seismic : REAL := 4500.0;
    
    // Typhoon Wind-Load Displacement Matrices (Lookup)
    // 10x10 matrix mapping wind speed and direction to expected steady-state displacement
    Wind_Disp_Matrix_X : ARRAY[0..9, 0..9] OF REAL; 
    Wind_Disp_Matrix_Y : ARRAY[0..9, 0..9] OF REAL;
    
    Target_Disp_X : REAL;
    Target_Disp_Y : REAL;
    
    // Timers
    S_Wave_Countdown : TON;
    Lockout_Timer : TON;
    
    // Internal variables
    Wind_Index_Speed : INT;
    Wind_Index_Dir : INT;
    Force_Demand_X : REAL;
    Force_Demand_Y : REAL;
    Max_Force : REAL := 8000.0; (* kN max hydraulic force *)
    
    Seismic_Precharge_Active : BOOL;
END_VAR

// -----------------------------------------------------------------------------
// Initialize Wind Displacement Matrices (Simplified for implementation)
// -----------------------------------------------------------------------------
IF State = 0 THEN
    // [Matrix initialization logic omitted for brevity, assumes pre-loaded]
    State := 1;
    System_Status := 'INITIALIZING';
END_IF;

// -----------------------------------------------------------------------------
// Safety & Interlocks
// -----------------------------------------------------------------------------
IF Emergency_Stop OR Hyd_Pressure < 150.0 OR Oil_Temp > 75.0 THEN
    Hyd_Command.Lock_Engaged := TRUE;
    Hyd_Command.Valve_Open_X := 0.0;
    Hyd_Command.Valve_Open_Y := 0.0;
    Hyd_Command.Actuator_Force_X := 0.0;
    Hyd_Command.Actuator_Force_Y := 0.0;
    Fault_Code := 16#FF01;
    System_Status := 'EMERGENCY_LOCKDOWN';
    RETURN;
END_IF;

IF NOT Enable THEN
    Hyd_Command.Lock_Engaged := FALSE; // Semi-active passive damping only
    Hyd_Command.Valve_Open_X := 50.0; // Neutral damping
    Hyd_Command.Valve_Open_Y := 50.0;
    System_Status := 'PASSIVE_MODE';
    RETURN;
END_IF;

// -----------------------------------------------------------------------------
// 1. Seismic P-Wave Early Warning Network Integration
// -----------------------------------------------------------------------------
// The P-Wave arrives before the destructive S-Wave. We use this time to 
// unlock the mass, pre-charge the hydraulics, and align the phase.
Seismic_Precharge_Active := FALSE;
Ready_For_Seismic := FALSE;

IF Seismic_Network.P_Wave_Detected AND Seismic_Network.Estimated_Magnitude > 4.5 THEN
    System_Status := 'SEISMIC_EARLY_WARNING_ACTIVE';
    Seismic_Precharge_Active := TRUE;
    
    S_Wave_Countdown(IN := TRUE, PT := Seismic_Network.Time_To_S_Wave);
    
    // Pre-condition the TMD: ensure it is perfectly centered and ready to counteract
    // the first S-wave displacement.
    IF NOT S_Wave_Countdown.Q THEN
        Target_Disp_X := 0.0;
        Target_Disp_Y := 0.0;
        // High gain to strictly hold center until impact
        Force_Demand_X := (Target_Disp_X - Pendulum_Sensors.Disp_X) * (Kp_Seismic * 1.5) - (Pendulum_Sensors.Vel_X * Kd_Seismic);
        Force_Demand_Y := (Target_Disp_Y - Pendulum_Sensors.Disp_Y) * (Kp_Seismic * 1.5) - (Pendulum_Sensors.Vel_Y * Kd_Seismic);
        Ready_For_Seismic := TRUE;
    ELSE
        // S-Wave has arrived, transition to active seismic damping
        Force_Demand_X := -(Bldg_Accel_X * 700000.0) - (Pendulum_Sensors.Vel_X * Kd_Seismic); // F = ma compensation
        Force_Demand_Y := -(Bldg_Accel_Y * 700000.0) - (Pendulum_Sensors.Vel_Y * Kd_Seismic);
    END_IF;
    
    Typhoon_Mode_Active := FALSE;

// -----------------------------------------------------------------------------
// 2. Typhoon Sustained Wind-Load Displacement Matrices
// -----------------------------------------------------------------------------
ELSIF Anemometer_Array.Sustained_Speed > 15.0 THEN
    System_Status := 'TYPHOON_MODE_ACTIVE';
    Typhoon_Mode_Active := TRUE;
    S_Wave_Countdown(IN := FALSE); // Reset
    
    // Map wind speed (15 to 70 m/s) to index 0-9
    Wind_Index_Speed := REAL_TO_INT((Anemometer_Array.Sustained_Speed - 15.0) / 5.5);
    IF Wind_Index_Speed > 9 THEN Wind_Index_Speed := 9; END_IF;
    IF Wind_Index_Speed < 0 THEN Wind_Index_Speed := 0; END_IF;
    
    // Map direction (0-359) to index 0-9
    Wind_Index_Dir := REAL_TO_INT(Anemometer_Array.Direction / 36.0);
    IF Wind_Index_Dir > 9 THEN Wind_Index_Dir := 9; END_IF;
    IF Wind_Index_Dir < 0 THEN Wind_Index_Dir := 0; END_IF;
    
    // Lookup target steady-state offset (matrix defines structural tilt under sustained wind)
    Target_Disp_X := Wind_Disp_Matrix_X[Wind_Index_Speed, Wind_Index_Dir];
    Target_Disp_Y := Wind_Disp_Matrix_Y[Wind_Index_Speed, Wind_Index_Dir];
    
    // Active PD Control around the wind-induced offset
    // This allows the 700-ton pendulum to counteract the harmonic vortex shedding
    Force_Demand_X := (Target_Disp_X - Pendulum_Sensors.Disp_X) * Kp_Wind - (Pendulum_Sensors.Vel_X * Kd_Wind);
    Force_Demand_Y := (Target_Disp_Y - Pendulum_Sensors.Disp_Y) * Kp_Wind - (Pendulum_Sensors.Vel_Y * Kd_Wind);

// -----------------------------------------------------------------------------
// 3. Normal Operation / Low Wind
// -----------------------------------------------------------------------------
ELSE
    System_Status := 'NORMAL_ACTIVE_DAMPING';
    Typhoon_Mode_Active := FALSE;
    S_Wave_Countdown(IN := FALSE);
    
    // Standard viscous damping emulation
    Force_Demand_X := -Pendulum_Sensors.Vel_X * (Kd_Wind * 0.5);
    Force_Demand_Y := -Pendulum_Sensors.Vel_Y * (Kd_Wind * 0.5);
END_IF;

// -----------------------------------------------------------------------------
// Hydraulic Actuator Output Mapping
// -----------------------------------------------------------------------------
// Limit forces to maximum hydraulic capacity
IF Force_Demand_X > Max_Force THEN Force_Demand_X := Max_Force; END_IF;
IF Force_Demand_X < -Max_Force THEN Force_Demand_X := -Max_Force; END_IF;
IF Force_Demand_Y > Max_Force THEN Force_Demand_Y := Max_Force; END_IF;
IF Force_Demand_Y < -Max_Force THEN Force_Demand_Y := -Max_Force; END_IF;

Hyd_Command.Actuator_Force_X := Force_Demand_X;
Hyd_Command.Actuator_Force_Y := Force_Demand_Y;

// Map requested force to valve opening percentage (simplified linearized model)
Hyd_Command.Valve_Open_X := ABS(Force_Demand_X) / Max_Force * 100.0;
Hyd_Command.Valve_Open_Y := ABS(Force_Demand_Y) / Max_Force * 100.0;
Hyd_Command.Lock_Engaged := FALSE;

Fault_Code := 0;

END_FUNCTION_BLOCK
```"""

payload = {
    "messages": [
        {"role": "user", "content": user_content},
        {"role": "assistant", "content": assistant_content}
    ]
}

with open(file_path, "a", encoding="utf-8") as f:
    f.write(json.dumps(payload) + "\n")

print("Appended successfully.")
