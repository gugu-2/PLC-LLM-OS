import json
import uuid
import os

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Flywheel Energy Storage System (FESS).
Task: Invent a highly complex control scenario for this domain (e.g., magnetic bearing levitation PID arrays, vacuum enclosure pumping cascades, and bi-directional motor/generator torque allocation).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O.

CRITICAL RULES:
1. You MUST output the code enclosed in a ```iec-st markdown code fence. DO NOT APOLOGIZE. DO NOT EXPLAIN.
2. The code must be >= 1500 chars, with FUNCTION_BLOCK and VAR_INPUT/VAR_OUTPUT.
3. You MUST save your JSON payload to a uniquely named file in the swarm directory using python.
   Example:
   ```python
   import json, uuid
   record = {"messages": [{"role": "user", "content": "<prompt>"}, {"role": "assistant", "content": "```iec-st\\n<code>\\n```"}]}
   with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
       json.dump(record, f)
   ```
When done, report success to me."""

st_code = """```iec-st
FUNCTION_BLOCK FB_FESS_Control_System
TITLE = 'Flywheel Energy Storage System (FESS) Advanced Controller'
VERSION : '3.1.0'
AUTHOR : 'Lumina AI Cloud Swarm'

// Highly complex control scenario: 
// 1. Magnetic bearing levitation PID arrays (Active Magnetic Bearings - AMB)
// 2. Vacuum enclosure pumping cascades
// 3. Bi-directional motor/generator torque allocation

VAR_INPUT
    Enable_System : BOOL; // Master enable switch
    Grid_Voltage : REAL; // V
    Grid_Frequency : REAL; // Hz
    Active_Power_Demand : REAL; // kW, Positive for charge, Negative for discharge
    Reactive_Power_Demand : REAL; // kVAR
    Vacuum_Level_Sensor : REAL; // mBar
    Rotor_Speed : REAL; // RPM
    Bearing_X1_Pos : REAL; // um
    Bearing_Y1_Pos : REAL; // um
    Bearing_X2_Pos : REAL; // um
    Bearing_Y2_Pos : REAL; // um
    Stator_Temp : REAL; // C
    Rotor_Temp_Est : REAL; // C
    Chiller_Temp : REAL; // C
END_VAR

VAR_OUTPUT
    System_Status : INT; // 0=Off, 1=Levitating, 2=Vacuum_Pump, 3=Charging, 4=Ready, 5=Discharging, 99=Fault
    Vacuum_Pump_1_Cmd : BOOL; // Roughing pump
    Vacuum_Pump_2_Cmd : BOOL; // Turbomolecular pump
    Bearing_X1_Current_Ref : REAL; // A
    Bearing_Y1_Current_Ref : REAL; // A
    Bearing_X2_Current_Ref : REAL; // A
    Bearing_Y2_Current_Ref : REAL; // A
    Inverter_Active : BOOL;
    Torque_Cmd : REAL; // Nm
    Chiller_Pump_Cmd : BOOL;
    Fault_Code : DWORD;
END_VAR

VAR
    // Internal States
    State : INT := 0; 
    Fault_Flag : BOOL := FALSE;
    
    // Magnetic Bearing PID Controllers
    PID_X1_Kp : REAL := 5.0; PID_X1_Ki : REAL := 0.1; PID_X1_Kd : REAL := 0.05;
    PID_Y1_Kp : REAL := 5.0; PID_Y1_Ki : REAL := 0.1; PID_Y1_Kd : REAL := 0.05;
    PID_X2_Kp : REAL := 5.0; PID_X2_Ki : REAL := 0.1; PID_X2_Kd : REAL := 0.05;
    PID_Y2_Kp : REAL := 5.0; PID_Y2_Ki : REAL := 0.1; PID_Y2_Kd : REAL := 0.05;
    
    Integ_X1 : REAL := 0.0; Prev_Err_X1 : REAL := 0.0;
    Integ_Y1 : REAL := 0.0; Prev_Err_Y1 : REAL := 0.0;
    Integ_X2 : REAL := 0.0; Prev_Err_X2 : REAL := 0.0;
    Integ_Y2 : REAL := 0.0; Prev_Err_Y2 : REAL := 0.0;
    
    // Limits
    Max_Bearing_Current : REAL := 15.0; // A
    Max_Rotor_Speed : REAL := 60000.0; // RPM
    Min_Vacuum_Level : REAL := 1e-4; // mBar
    
    // Torque Allocation
    Rated_Torque : REAL := 500.0; // Nm
    Inertia : REAL := 10.5; // kg*m^2
END_VAR

// -----------------------------------------------------------------------------
// 1. MAGNETIC BEARING LEVITATION PID ARRAYS
// -----------------------------------------------------------------------------
// Target position is 0.0 um for all axes
IF Enable_System THEN
    // X1 Axis
    Integ_X1 := Integ_X1 + (0.0 - Bearing_X1_Pos);
    Bearing_X1_Current_Ref := (PID_X1_Kp * (0.0 - Bearing_X1_Pos)) + (PID_X1_Ki * Integ_X1) + (PID_X1_Kd * ((0.0 - Bearing_X1_Pos) - Prev_Err_X1));
    Prev_Err_X1 := (0.0 - Bearing_X1_Pos);
    
    // Y1 Axis
    Integ_Y1 := Integ_Y1 + (0.0 - Bearing_Y1_Pos);
    Bearing_Y1_Current_Ref := (PID_Y1_Kp * (0.0 - Bearing_Y1_Pos)) + (PID_Y1_Ki * Integ_Y1) + (PID_Y1_Kd * ((0.0 - Bearing_Y1_Pos) - Prev_Err_Y1));
    Prev_Err_Y1 := (0.0 - Bearing_Y1_Pos);

    // X2 Axis
    Integ_X2 := Integ_X2 + (0.0 - Bearing_X2_Pos);
    Bearing_X2_Current_Ref := (PID_X2_Kp * (0.0 - Bearing_X2_Pos)) + (PID_X2_Ki * Integ_X2) + (PID_X2_Kd * ((0.0 - Bearing_X2_Pos) - Prev_Err_X2));
    Prev_Err_X2 := (0.0 - Bearing_X2_Pos);
    
    // Y2 Axis
    Integ_Y2 := Integ_Y2 + (0.0 - Bearing_Y2_Pos);
    Bearing_Y2_Current_Ref := (PID_Y2_Kp * (0.0 - Bearing_Y2_Pos)) + (PID_Y2_Ki * Integ_Y2) + (PID_Y2_Kd * ((0.0 - Bearing_Y2_Pos) - Prev_Err_Y2));
    Prev_Err_Y2 := (0.0 - Bearing_Y2_Pos);
    
    // Saturation
    IF Bearing_X1_Current_Ref > Max_Bearing_Current THEN Bearing_X1_Current_Ref := Max_Bearing_Current; ELSIF Bearing_X1_Current_Ref < -Max_Bearing_Current THEN Bearing_X1_Current_Ref := -Max_Bearing_Current; END_IF;
    IF Bearing_Y1_Current_Ref > Max_Bearing_Current THEN Bearing_Y1_Current_Ref := Max_Bearing_Current; ELSIF Bearing_Y1_Current_Ref < -Max_Bearing_Current THEN Bearing_Y1_Current_Ref := -Max_Bearing_Current; END_IF;
    IF Bearing_X2_Current_Ref > Max_Bearing_Current THEN Bearing_X2_Current_Ref := Max_Bearing_Current; ELSIF Bearing_X2_Current_Ref < -Max_Bearing_Current THEN Bearing_X2_Current_Ref := -Max_Bearing_Current; END_IF;
    IF Bearing_Y2_Current_Ref > Max_Bearing_Current THEN Bearing_Y2_Current_Ref := Max_Bearing_Current; ELSIF Bearing_Y2_Current_Ref < -Max_Bearing_Current THEN Bearing_Y2_Current_Ref := -Max_Bearing_Current; END_IF;
ELSE
    Bearing_X1_Current_Ref := 0.0; Bearing_Y1_Current_Ref := 0.0;
    Bearing_X2_Current_Ref := 0.0; Bearing_Y2_Current_Ref := 0.0;
END_IF;

// -----------------------------------------------------------------------------
// 2. VACUUM ENCLOSURE PUMPING CASCADES
// -----------------------------------------------------------------------------
IF Enable_System THEN
    IF Vacuum_Level_Sensor > 10.0 THEN
        Vacuum_Pump_1_Cmd := TRUE; // Roughing pump on
        Vacuum_Pump_2_Cmd := FALSE;
        IF State < 2 THEN State := 2; END_IF;
    ELSIF Vacuum_Level_Sensor <= 10.0 AND Vacuum_Level_Sensor > Min_Vacuum_Level THEN
        Vacuum_Pump_1_Cmd := TRUE; // Backing roughing pump
        Vacuum_Pump_2_Cmd := TRUE; // Turbo pump on
    ELSE
        Vacuum_Pump_1_Cmd := FALSE;
        Vacuum_Pump_2_Cmd := TRUE; // Maintain high vacuum
    END_IF;
ELSE
    Vacuum_Pump_1_Cmd := FALSE;
    Vacuum_Pump_2_Cmd := FALSE;
END_IF;

// -----------------------------------------------------------------------------
// 3. BI-DIRECTIONAL MOTOR/GENERATOR TORQUE ALLOCATION
// -----------------------------------------------------------------------------
IF Enable_System AND NOT Fault_Flag AND (Vacuum_Level_Sensor <= Min_Vacuum_Level * 10.0) THEN
    Inverter_Active := TRUE;
    
    // Calculate Torque Command based on Active Power Demand
    // P (W) = Torque (Nm) * Omega (rad/s)
    // Omega = Rotor_Speed * 2 * 3.14159 / 60
    IF Rotor_Speed > 1000.0 THEN
        Torque_Cmd := (Active_Power_Demand * 1000.0) / (Rotor_Speed * 0.104719755); 
    ELSE
        Torque_Cmd := 0.0; // Prevent divide by zero / excessive torque at low speed
    END_IF;
    
    // Enforce Limits
    IF Torque_Cmd > Rated_Torque THEN
        Torque_Cmd := Rated_Torque;
    ELSIF Torque_Cmd < -Rated_Torque THEN
        Torque_Cmd := -Rated_Torque;
    END_IF;
    
    // State machine updates
    IF Torque_Cmd > 0.0 THEN
        State := 3; // Charging
    ELSIF Torque_Cmd < 0.0 THEN
        State := 5; // Discharging
    ELSE
        State := 4; // Ready/Standby
    END_IF;
ELSE
    Inverter_Active := FALSE;
    Torque_Cmd := 0.0;
    IF NOT Enable_System THEN State := 0; END_IF;
END_IF;

// -----------------------------------------------------------------------------
// 4. THERMAL MANAGEMENT & FAULT HANDLING
// -----------------------------------------------------------------------------
IF Stator_Temp > 85.0 OR Rotor_Temp_Est > 120.0 THEN
    Chiller_Pump_Cmd := TRUE;
ELSE
    Chiller_Pump_Cmd := FALSE;
END_IF;

// Faults
IF Rotor_Speed > Max_Rotor_Speed THEN
    Fault_Flag := TRUE;
    Fault_Code := 16#00000001; // Overspeed
ELSIF Stator_Temp > 105.0 THEN
    Fault_Flag := TRUE;
    Fault_Code := 16#00000002; // Overtemp
ELSIF (Bearing_X1_Pos > 100.0) OR (Bearing_X1_Pos < -100.0) OR (Bearing_Y1_Pos > 100.0) OR (Bearing_Y1_Pos < -100.0) THEN
    Fault_Flag := TRUE;
    Fault_Code := 16#00000004; // Bearing deviation
END_IF;

IF Fault_Flag THEN
    System_Status := 99;
    Inverter_Active := FALSE;
    Torque_Cmd := 0.0;
    Enable_System := FALSE; // Trip
ELSE
    System_Status := State;
END_IF;

END_FUNCTION_BLOCK
```"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": st_code}
    ]
}

os.makedirs("data/swarm_raw", exist_ok=True)

with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\n")

with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
    json.dump(record, f)

print('Success')
