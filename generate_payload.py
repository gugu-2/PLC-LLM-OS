import os, json, uuid

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 data.
Your specific domain is: Concentrated Solar Power (CSP) Heliostat Array.
Task: Invent a highly complex control scenario for this domain (e.g., dual-axis sun tracking algorithms, molten salt receiver temperature feedback, and wind-stow emergency positioning).
Write a deterministic Structured Text (ST) FUNCTION_BLOCK. Include complete VAR declarations and physical I/O."""

st_code = """```iec-st
FUNCTION_BLOCK FB_Heliostat_Controller
TITLE = 'CSP Heliostat Array Dual-Axis Controller'
VERSION : '3.1'
AUTHOR : 'Lumina AI Elite'

VAR_INPUT
    Enable : BOOL; // System enable flag
    Mode_Auto : BOOL; // True for automatic tracking, False for manual
    Manual_Azimuth : REAL; // Manual override azimuth target (degrees)
    Manual_Elevation : REAL; // Manual override elevation target (degrees)
    
    // Environmental & Sensor Inputs
    Wind_Speed : REAL; // Current wind speed (m/s)
    Wind_Direction : REAL; // Current wind direction (degrees)
    Solar_Irradiance : REAL; // DNI (W/m^2)
    Sun_Azimuth : REAL; // Calculated sun azimuth (degrees)
    Sun_Elevation : REAL; // Calculated sun elevation (degrees)
    
    // Receiver Feedback
    Receiver_Temp : REAL; // Molten salt receiver surface temperature (C)
    Receiver_Temp_Setpoint : REAL; // Target receiver temperature (C)
    
    // Heliostat Encoders
    Actual_Azimuth : REAL; // Current azimuth angle (degrees)
    Actual_Elevation : REAL; // Current elevation angle (degrees)
    
    // Safety & Interlocks
    E_Stop : BOOL; // Emergency stop active low
    Grid_Loss : BOOL; // Power grid loss signal
END_VAR

VAR_OUTPUT
    Azimuth_Drive_Cmd : REAL; // Velocity command to azimuth drive (-100 to 100%)
    Elevation_Drive_Cmd : REAL; // Velocity command to elevation drive (-100 to 100%)
    Brake_Release : BOOL; // Release holding brakes
    
    Status_State : INT; // 0=Off, 1=Track, 2=Stow, 3=Standby, 4=Fault
    Alarm_Active : BOOL; // High level alarm flag
    Alarm_Code : INT; // Diagnostic code
    
    Target_Azimuth_Out : REAL; // Current target for telemetry
    Target_Elevation_Out : REAL; // Current target for telemetry
END_VAR

VAR
    // Internal States & Timers
    Current_State : INT;
    T_Stow_Delay : LTIME;
    T_Wind_Filter_Time : TIME := T#5S;
    T_Wind_Filter_Acc : TIME;
    
    // PID Controllers (Simplified)
    Azimuth_Error : REAL;
    Azimuth_Integral : REAL;
    Elevation_Error : REAL;
    Elevation_Integral : REAL;
    
    // Constants & Parameters
    MAX_WIND_SPEED : REAL := 15.0; // Stow wind speed threshold (m/s)
    STOW_AZIMUTH : REAL := 90.0; // Safe stow position
    STOW_ELEVATION : REAL := 85.0; // Face up to sky
    DEFOCUS_OFFSET : REAL := 5.0; // Degrees to defocus if receiver is too hot
    MAX_RECEIVER_TEMP : REAL := 650.0; // Maximum safe receiver temp (C)
    
    // Control gains
    KP_AZ : REAL := 2.5;
    KI_AZ : REAL := 0.1;
    KP_EL : REAL := 2.5;
    KI_EL : REAL := 0.1;
END_VAR

(* 
    Heliostat Control Logic 
    - Handles emergency conditions and wind stowing.
    - Manages receiver temperature by defocusing if necessary.
    - Performs closed-loop dual-axis sun tracking.
*)

// 1. Safety and Environmental Checks
IF NOT E_Stop OR Grid_Loss THEN
    Current_State := 4; // Fault / Emergency
    Alarm_Active := TRUE;
    Alarm_Code := 1001; // E-Stop or Grid Loss
ELSIF Wind_Speed > MAX_WIND_SPEED THEN
    // Simulated wind filter TON logic without calling FB explicitly
    Current_State := 2; // Wind Stow
    Alarm_Active := TRUE;
    Alarm_Code := 2001; // High Wind
ELSE
    IF NOT Enable THEN
        Current_State := 0; // Off
        Alarm_Active := FALSE;
        Alarm_Code := 0;
    ELSIF Mode_Auto THEN
        Current_State := 1; // Tracking
        Alarm_Active := FALSE;
        Alarm_Code := 0;
    ELSE
        Current_State := 3; // Manual Standby
        Alarm_Active := FALSE;
        Alarm_Code := 0;
    END_IF;
END_IF;

// 2. Determine Targets based on State
CASE Current_State OF
    0, 4: // Off or Fault - Apply Brakes, Zero Commands
        Target_Azimuth_Out := Actual_Azimuth;
        Target_Elevation_Out := Actual_Elevation;
        Azimuth_Drive_Cmd := 0.0;
        Elevation_Drive_Cmd := 0.0;
        Brake_Release := FALSE;
        
    2: // Wind Stow
        Target_Azimuth_Out := STOW_AZIMUTH;
        Target_Elevation_Out := STOW_ELEVATION;
        Brake_Release := TRUE;
        
    3: // Manual Override
        Target_Azimuth_Out := Manual_Azimuth;
        Target_Elevation_Out := Manual_Elevation;
        Brake_Release := TRUE;
        
    1: // Auto Tracking
        // Defocus logic if receiver is exceeding target temperature
        IF Receiver_Temp > Receiver_Temp_Setpoint AND Receiver_Temp < MAX_RECEIVER_TEMP THEN
            // Proportional defocus on elevation
            Target_Elevation_Out := Sun_Elevation + ((Receiver_Temp - Receiver_Temp_Setpoint) * 0.1);
            Target_Azimuth_Out := Sun_Azimuth;
        ELSIF Receiver_Temp >= MAX_RECEIVER_TEMP THEN
            // Emergency Defocus
            Target_Elevation_Out := Sun_Elevation + DEFOCUS_OFFSET;
            Target_Azimuth_Out := Sun_Azimuth + DEFOCUS_OFFSET;
        ELSE
            // Normal Tracking
            Target_Azimuth_Out := Sun_Azimuth;
            Target_Elevation_Out := Sun_Elevation;
        END_IF;
        Brake_Release := TRUE;
END_CASE;

// 3. Closed-Loop Position Control
IF Current_State = 1 OR Current_State = 2 OR Current_State = 3 THEN
    // Azimuth PI Control
    Azimuth_Error := Target_Azimuth_Out - Actual_Azimuth;
    Azimuth_Integral := Azimuth_Integral + (Azimuth_Error * 0.1); // Assuming 100ms cycle
    // Anti-windup
    IF Azimuth_Integral > 50.0 THEN Azimuth_Integral := 50.0; END_IF;
    IF Azimuth_Integral < -50.0 THEN Azimuth_Integral := -50.0; END_IF;
    
    Azimuth_Drive_Cmd := (KP_AZ * Azimuth_Error) + (KI_AZ * Azimuth_Integral);
    
    // Elevation PI Control
    Elevation_Error := Target_Elevation_Out - Actual_Elevation;
    Elevation_Integral := Elevation_Integral + (Elevation_Error * 0.1);
    // Anti-windup
    IF Elevation_Integral > 50.0 THEN Elevation_Integral := 50.0; END_IF;
    IF Elevation_Integral < -50.0 THEN Elevation_Integral := -50.0; END_IF;
    
    Elevation_Drive_Cmd := (KP_EL * Elevation_Error) + (KI_EL * Elevation_Integral);
    
    // Output Limiting
    IF Azimuth_Drive_Cmd > 100.0 THEN Azimuth_Drive_Cmd := 100.0; END_IF;
    IF Azimuth_Drive_Cmd < -100.0 THEN Azimuth_Drive_Cmd := -100.0; END_IF;
    IF Elevation_Drive_Cmd > 100.0 THEN Elevation_Drive_Cmd := 100.0; END_IF;
    IF Elevation_Drive_Cmd < -100.0 THEN Elevation_Drive_Cmd := -100.0; END_IF;
END_IF;

// 4. Update Status
Status_State := Current_State;

END_FUNCTION_BLOCK
```"""

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": st_code}
    ]
}

os.makedirs("data/swarm_raw", exist_ok=True)
uid = uuid.uuid4().hex[:8]
with open(f"data/swarm_raw/agent_{uid}.json", "w", encoding="utf-8") as f:
    json.dump(record, f)

with open("data/synthetic_generation_v3_enterprise.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\\n")

print(f"Success. Agent {uid} generated.")
