import json
import os

response_content = """Here is the evolved IEC 61131-3 Structured Text (ST) implementation for the Mars Rover Controller. This module integrates the Rocker-Bogie kinematics with independent steering and drive control, IMU-based loose regolith slip-compensation, and RTG thermal management.

```iecst
TYPE
    // Kinematic constraints for the 6 wheels
    // Indexes: 1=FrontLeft, 2=FrontRight, 3=MidLeft, 4=MidRight, 5=RearLeft, 6=RearRight
    st_Wheel_Config : STRUCT
        PosX : REAL; // X distance from Center of Mass (m)
        PosY : REAL; // Y distance from Center of Mass (m)
        Radius : REAL; // Wheel radius (m)
        Max_Steer_Angle : REAL; // Radians
    END_STRUCT;
    
    st_IMU_Data : STRUCT
        AccelX : REAL; // Linear acceleration (m/s^2)
        AccelY : REAL;
        AccelZ : REAL;
        Pitch : REAL; // Radians
        Roll : REAL;
        YawRate : REAL; // Rad/s
    END_STRUCT;
    
    st_RTG_Telemetry : STRUCT
        CoreTemp : REAL; // Celsius
        ColdJunctionTemp : REAL; 
        RadiatorTemps : ARRAY[1..4] OF REAL;
        PowerOutput : REAL; // Watts
    END_STRUCT;
END_TYPE

// ======================================================================
// FUNCTION BLOCK: Advanced PID with Anti-Windup & Saturation
// ======================================================================
FUNCTION_BLOCK FB_Advanced_PID
VAR_INPUT
    Setpoint : REAL;
    Feedback : REAL;
    Kp : REAL;
    Ki : REAL;
    Kd : REAL;
    Dt : REAL;
    OutMin : REAL;
    OutMax : REAL;
    Reset : BOOL;
END_VAR
VAR_OUTPUT
    Output : REAL;
END_VAR
VAR
    Integral : REAL;
    PrevError : REAL;
    Error : REAL;
    Derivative : REAL;
END_VAR
BEGIN
    IF Reset THEN
        Integral := 0.0;
        PrevError := 0.0;
        Output := 0.0;
        RETURN;
    END_IF;
    
    Error := Setpoint - Feedback;
    
    // Anti-windup
    IF ((Output < OutMax) AND (Error > 0.0)) OR ((Output > OutMin) AND (Error < 0.0)) THEN
        Integral := Integral + (Error * Dt);
    END_IF;
    
    IF Dt > 0.0 THEN
        Derivative := (Error - PrevError) / Dt;
    ELSE
        Derivative := 0.0;
    END_IF;
    
    Output := (Kp * Error) + (Ki * Integral) + (Kd * Derivative);
    
    // Saturation limiters
    IF Output > OutMax THEN Output := OutMax; END_IF;
    IF Output < OutMin THEN Output := OutMin; END_IF;
    
    PrevError := Error;
END_FUNCTION_BLOCK

// ======================================================================
// FUNCTION BLOCK: Mars Rover Rocker-Bogie & Thermal Controller
// ======================================================================
FUNCTION_BLOCK FB_MarsRover_DriveController
TITLE = 'JPL-Grade Rocker-Bogie 6-Wheel Controller'
VERSION : '2.0'
AUTHOR : 'Lumina Space Systems'

VAR_INPUT
    // Command Intention
    Cmd_Vel_X : REAL; // Target forward velocity [m/s]
    Cmd_Vel_Y : REAL; // Target lateral velocity [m/s] (for crab steering)
    Cmd_YawRate : REAL; // Target rotation [rad/s]
    
    // Sensor Telemetry
    Enc_Steer_Pos : ARRAY[1..6] OF REAL; // Absolute steering angle [rad]
    Enc_Drive_Vel : ARRAY[1..6] OF REAL; // Wheel angular velocity [rad/s]
    IMU : st_IMU_Data;
    RTG : st_RTG_Telemetry;
    
    // Config
    Cycle_Dt : REAL := 0.01; // 10ms execution cycle
    
    // System control
    Sys_Enable : BOOL;
    Sys_Reset : BOOL;
END_VAR

VAR_OUTPUT
    // Actuator Commands
    Cmd_Steer_Torque : ARRAY[1..6] OF REAL; // Commanded steering motor effort
    Cmd_Drive_Torque : ARRAY[1..6] OF REAL; // Commanded drive motor torque
    
    // Thermal Subsystem Commands
    Cmd_PrimaryPumpSpeed : REAL; // PWM %
    Cmd_RadiatorValves : ARRAY[1..4] OF BOOL;
    
    // Diagnostics & State
    Est_Ground_Speed : REAL; // Fusion of IMU and Odometry
    Slip_Flags : ARRAY[1..6] OF BOOL;
    Loose_Regolith_Detected : BOOL;
END_VAR

VAR
    // Kinematic Configuration Matrix
    Wheels : ARRAY[1..6] OF st_Wheel_Config := [
        (PosX:= 1.2, PosY:= 1.0, Radius:=0.25, Max_Steer_Angle:=1.57), // FL
        (PosX:= 1.2, PosY:=-1.0, Radius:=0.25, Max_Steer_Angle:=1.57), // FR
        (PosX:= 0.0, PosY:= 1.1, Radius:=0.25, Max_Steer_Angle:=1.57), // ML (Fully steerable crab mod)
        (PosX:= 0.0, PosY:=-1.1, Radius:=0.25, Max_Steer_Angle:=1.57), // MR
        (PosX:=-1.2, PosY:= 1.0, Radius:=0.25, Max_Steer_Angle:=1.57), // RL
        (PosX:=-1.2, PosY:=-1.0, Radius:=0.25, Max_Steer_Angle:=1.57)  // RR
    ];
    
    // Targets
    Tgt_Steer_Angle : ARRAY[1..6] OF REAL;
    Tgt_Wheel_Vel : ARRAY[1..6] OF REAL;
    
    // Controller Instances
    Steer_PID : ARRAY[1..6] OF FB_Advanced_PID;
    Drive_PID : ARRAY[1..6] OF FB_Advanced_PID;
    Thermal_PID : FB_Advanced_PID;
    
    // State Estimation & Slip Metrics
    IMU_Vel_X : REAL;
    Odom_Vel_X : ARRAY[1..6] OF REAL;
    Avg_Odom_Vel : REAL;
    Slip_Ratio : ARRAY[1..6] OF REAL;
    
    i : INT;
    v_x_wheel, v_y_wheel : REAL;
    Slip_Threshold : REAL := 0.25; // 25% slip marks loose regolith threshold
END_VAR

BEGIN
    // Handle system resets
    IF Sys_Reset THEN
        IMU_Vel_X := 0.0;
        FOR i := 1 TO 6 DO
            Steer_PID[i](Reset := TRUE);
            Drive_PID[i](Reset := TRUE);
        END_FOR;
        Thermal_PID(Reset := TRUE);
    END_IF;

    // Safety Interlock
    IF NOT Sys_Enable THEN
        FOR i := 1 TO 6 DO
            Cmd_Steer_Torque[i] := 0.0;
            Cmd_Drive_Torque[i] := 0.0;
        END_FOR;
        Cmd_PrimaryPumpSpeed := 0.0;
        RETURN;
    END_IF;

    // ==========================================
    // 1. KINEMATICS & DRIVE SYNC
    // ==========================================
    FOR i := 1 TO 6 DO
        // Transform chassis velocity commands into individual wheel vectors
        v_x_wheel := Cmd_Vel_X - (Cmd_YawRate * Wheels[i].PosY);
        v_y_wheel := Cmd_Vel_Y + (Cmd_YawRate * Wheels[i].PosX);
        
        // Calculate Target Steering Angle (ATAN2 implementation for ST)
        IF ABS(v_x_wheel) > 0.001 OR ABS(v_y_wheel) > 0.001 THEN
            IF v_x_wheel > 0.0 THEN
                Tgt_Steer_Angle[i] := ATAN(v_y_wheel / v_x_wheel);
            ELSIF v_x_wheel < 0.0 AND v_y_wheel >= 0.0 THEN
                Tgt_Steer_Angle[i] := ATAN(v_y_wheel / v_x_wheel) + 3.14159;
            ELSIF v_x_wheel < 0.0 AND v_y_wheel < 0.0 THEN
                Tgt_Steer_Angle[i] := ATAN(v_y_wheel / v_x_wheel) - 3.14159;
            ELSIF v_x_wheel = 0.0 AND v_y_wheel > 0.0 THEN
                Tgt_Steer_Angle[i] := 1.5708;
            ELSIF v_x_wheel = 0.0 AND v_y_wheel < 0.0 THEN
                Tgt_Steer_Angle[i] := -1.5708;
            END_IF;
        ELSE
            Tgt_Steer_Angle[i] := Enc_Steer_Pos[i]; // Retain angle if stationary
        END_IF;
        
        // Target Wheel Angular Velocity [rad/s]
        Tgt_Wheel_Vel[i] := SQRT((v_x_wheel * v_x_wheel) + (v_y_wheel * v_y_wheel)) / Wheels[i].Radius;
        
        // Direction adjustment optimization: If target steering exceeds 90 degrees (1.57 rad),
        // flip the phase by 180 deg and reverse motor to avoid long steering sweeps.
        IF ABS(Tgt_Steer_Angle[i] - Enc_Steer_Pos[i]) > 1.5708 THEN
            IF Tgt_Steer_Angle[i] > 0.0 THEN
                Tgt_Steer_Angle[i] := Tgt_Steer_Angle[i] - 3.14159;
            ELSE
                Tgt_Steer_Angle[i] := Tgt_Steer_Angle[i] + 3.14159;
            END_IF;
            Tgt_Wheel_Vel[i] := -Tgt_Wheel_Vel[i];
        END_IF;
    END_FOR;

    // ==========================================
    // 2. SLIP COMPENSATION (LOOSE REGOLITH)
    // ==========================================
    // Integrating IMU Accel to estimate actual ground speed in the chassis X frame
    IMU_Vel_X := IMU_Vel_X + (IMU.AccelX * Cycle_Dt);
    
    // Odometry extraction via drive encoders
    Avg_Odom_Vel := 0.0;
    FOR i := 1 TO 6 DO
        Odom_Vel_X[i] := Enc_Drive_Vel[i] * Wheels[i].Radius * COS(Enc_Steer_Pos[i]);
        Avg_Odom_Vel := Avg_Odom_Vel + Odom_Vel_X[i];
    END_FOR;
    Avg_Odom_Vel := Avg_Odom_Vel / 6.0;
    
    // Complementary Filter: Trust IMU for transient changes, Odometry for steady-state (preventing integration drift)
    Est_Ground_Speed := (0.95 * IMU_Vel_X) + (0.05 * Avg_Odom_Vel);
    IMU_Vel_X := Est_Ground_Speed; // update internal state
    
    Loose_Regolith_Detected := FALSE;
    FOR i := 1 TO 6 DO
        // Calculate Slip Ratio 
        IF ABS(Tgt_Wheel_Vel[i]) > 0.1 THEN
            Slip_Ratio[i] := (Odom_Vel_X[i] - Est_Ground_Speed) / MAX(ABS(Odom_Vel_X[i]), 0.01);
        ELSE
            Slip_Ratio[i] := 0.0;
        END_IF;
        
        IF Slip_Ratio[i] > Slip_Threshold THEN
            Slip_Flags[i] := TRUE;
            Loose_Regolith_Detected := TRUE;
            // Traction Control Algorithm: Reduce target speed for slipping wheel to regain grip
            Tgt_Wheel_Vel[i] := Tgt_Wheel_Vel[i] * (1.0 - (Slip_Ratio[i] * 0.5)); 
        ELSE
            Slip_Flags[i] := FALSE;
        END_IF;
    END_FOR;

    // ==========================================
    // 3. ACTUATOR PID EXECUTION
    // ==========================================
    FOR i := 1 TO 6 DO
        // Steering Motor Control
        Steer_PID[i](
            Setpoint := Tgt_Steer_Angle[i],
            Feedback := Enc_Steer_Pos[i],
            Kp := 60.0, Ki := 5.0, Kd := 2.0,
            Dt := Cycle_Dt,
            OutMin := -100.0, OutMax := 100.0,
            Reset := Sys_Reset,
            Output => Cmd_Steer_Torque[i]
        );
        
        // Drive Motor Control
        Drive_PID[i](
            Setpoint := Tgt_Wheel_Vel[i],
            Feedback := Enc_Drive_Vel[i],
            Kp := 25.0, Ki := 2.5, Kd := 1.0,
            Dt := Cycle_Dt,
            OutMin := -100.0, OutMax := 100.0,
            Reset := Sys_Reset,
            Output => Cmd_Drive_Torque[i]
        );
    END_FOR;

    // ==========================================
    // 4. RTG THERMAL SHEDDING LOOP
    // ==========================================
    // PID Loop to maintain RTG core at nominal ~750°C by modulating coolant pump flow
    Thermal_PID(
        Setpoint := 750.0,
        Feedback := RTG.CoreTemp,
        Kp := 1.5, Ki := 0.05, Kd := 0.2,
        Dt := Cycle_Dt,
        OutMin := 0.0, // Unidirectional pumping
        OutMax := 100.0,
        Reset := Sys_Reset,
        Output => Cmd_PrimaryPumpSpeed
    );
    
    // Regulate flow to radiators dynamically
    IF RTG.ColdJunctionTemp > 200.0 THEN
        // Open all valves to shed heat rapidly
        FOR i := 1 TO 4 DO
            Cmd_RadiatorValves[i] := TRUE;
        END_FOR;
    ELSIF RTG.ColdJunctionTemp < 120.0 THEN
        // Isolate radiators to preserve heat in deep-cold environments (e.g. Martian night)
        FOR i := 1 TO 4 DO
            Cmd_RadiatorValves[i] := FALSE;
        END_FOR;
    END_IF;

END_FUNCTION_BLOCK
```"""

data = {
    "messages": [
        {
            "role": "user",
            "content": "You are acting as a Lead Robotics Engineer for a Planetary Rover (e.g., NASA JPL). Evolve a basic PID into a Mars Rover Rocker-Bogie Suspension and Drive Controller. Technical Specs: 1. 6-wheel independent steering and drive sync using absolute encoders. 2. Slip-compensation algorithms using IMU data to detect loose regolith. 3. Radioisotope Thermoelectric Generator (RTG) thermal shedding loops. Append to synthetic_generation_v3_enterprise.jsonl"
        },
        {
            "role": "assistant",
            "content": response_content
        }
    ]
}

target_file = r"C:\Users\majip\Downloads\LLM REASEARCH\data\synthetic_generation_v3_enterprise.jsonl"
os.makedirs(os.path.dirname(target_file), exist_ok=True)
with open(target_file, "a", encoding="utf-8") as f:
    f.write(json.dumps(data) + "\n")

print("Successfully written to", target_file)
