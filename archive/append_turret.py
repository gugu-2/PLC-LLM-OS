# -*- coding: utf-8 -*-
import json

user_prompt = """You are acting as a Lead Marine Engineer for a massive Floating Production Storage and Offloading (FPSO) vessel. Evolve a basic fluid block into a Subsea Turret Mooring and Swivel Controller. Technical Specs: 1. Multiphase crude oil flow routing across rotating high-pressure swivels. 2. Turret bearing lubrication and wear-debris monitoring. 3. Active heading control (weathervaning) utilizing azimuth thrusters. Append to synthetic_generation_v3_enterprise.jsonl."""

assistant_response = """\
(* 
==================================================================================================
Subsea Turret Mooring and Swivel Controller for FPSO Vessels
==================================================================================================
This block handles the critical functions of an FPSO Turret system:
1. Multiphase crude flow management and swivel seal integrity monitoring.
2. Turret bearing lubrication and wear-debris analysis.
3. Active Weathervaning Control via Azimuth Thrusters to minimize mooring line tension.
*)

TYPE ST_SwivelData :
STRUCT
    PrimarySealPressure      : REAL; (* barg *)
    SecondarySealPressure    : REAL; (* barg *)
    FlowRate                 : REAL; (* m3/hr *)
    Temperature              : REAL; (* deg C *)
    MultiphaseVFD_Feedback   : REAL; (* % *)
END_STRUCT
END_TYPE

TYPE ST_BearingLubeData :
STRUCT
    PumpPressure             : REAL; (* barg *)
    OilTemperature           : REAL; (* deg C *)
    WearDebrisPPM            : REAL; (* Particulates per million *)
    SumpLevel                : REAL; (* % *)
END_STRUCT
END_TYPE

TYPE ST_ThrusterCommand :
STRUCT
    Enable                   : BOOL;
    AzimuthAngleSetpoint     : REAL; (* Degrees 0-359.9 *)
    ThrustSetpoint           : REAL; (* % 0-100 *)
END_STRUCT
END_TYPE

TYPE ST_VesselHeading :
STRUCT
    CurrentVesselHeading     : REAL; (* Gyrocompass heading *)
    OptimalWindHeading       : REAL; (* Calculated wind optimal *)
    OptimalWaveHeading       : REAL; (* Calculated wave optimal *)
    CombinedOptimalHeading   : REAL; (* Resultant weathervaning target *)
    TurretAngleRelative      : REAL; (* Relative angle between turret and vessel *)
END_STRUCT
END_TYPE

FUNCTION_BLOCK FB_FPSO_TurretSwivelController
VAR_INPUT
    EnableSystem             : BOOL;
    
    // Sensor Inputs
    SwivelSensors            : ARRAY[1..4] OF ST_SwivelData; // 4 Multiphase swivels
    BearingSensors           : ARRAY[1..2] OF ST_BearingLubeData; // Forward and Aft turret bearings
    HeadingSensors           : ST_VesselHeading;
    
    // Setpoints
    MaxSealLeakPressure      : REAL := 15.0; // barg
    MaxWearDebris            : REAL := 500.0; // ppm
    HeadingDeadband          : REAL := 5.0;  // Degrees
END_VAR

VAR_OUTPUT
    // Swivel and Flow Control
    RoutingValves            : ARRAY[1..4] OF BOOL;
    EmergencyShutdownSwivel  : BOOL;
    
    // Bearing Lube
    LubePumpRun              : ARRAY[1..2] OF BOOL;
    BearingCriticalAlarm     : BOOL;
    
    // Thruster Control
    AftThrusterCmd           : ST_ThrusterCommand;
    FwdThrusterCmd           : ST_ThrusterCommand;
    
    // System Status
    SystemHealthy            : BOOL;
    HeadingError             : REAL;
END_VAR

VAR
    i : INT;
    HeadingDiff : REAL;
    PID_Integral : REAL;
    Kp : REAL := 2.0;
    Ki : REAL := 0.05;
END_VAR

// -----------------------------------------------------------------------------
// 1. Multiphase Crude Oil Flow Routing & Swivel Seal Monitoring
// -----------------------------------------------------------------------------
EmergencyShutdownSwivel := FALSE;

FOR i := 1 TO 4 DO
    // Default route open if system enabled
    RoutingValves[i] := EnableSystem;
    
    // Check seal integrity: if secondary seal pressure rises, primary seal is leaking
    IF SwivelSensors[i].SecondarySealPressure > MaxSealLeakPressure THEN
        // Isolate the faulty swivel to prevent catastrophic crude leak to sea
        RoutingValves[i] := FALSE;
    END_IF;
    
    // Extreme temperature or catastrophic failure
    IF SwivelSensors[i].Temperature > 90.0 OR SwivelSensors[i].PrimarySealPressure > 350.0 THEN
        EmergencyShutdownSwivel := TRUE;
    END_IF;
END_FOR;

// -----------------------------------------------------------------------------
// 2. Turret Bearing Lubrication & Wear-Debris Monitoring
// -----------------------------------------------------------------------------
BearingCriticalAlarm := FALSE;

FOR i := 1 TO 2 DO
    // Auto start/stop lube pump based on pressure and system enable
    IF EnableSystem AND BearingSensors[i].PumpPressure < 4.0 THEN
        LubePumpRun[i] := TRUE;
    ELSIF BearingSensors[i].PumpPressure > 6.5 THEN
        LubePumpRun[i] := FALSE;
    END_IF;
    
    // Wear Debris Analysis (Condition Monitoring)
    IF BearingSensors[i].WearDebrisPPM > MaxWearDebris THEN
        BearingCriticalAlarm := TRUE;
        // In a real scenario, this might restrict turret rotation speed
    END_IF;
END_FOR;

// -----------------------------------------------------------------------------
// 3. Active Heading Control (Weathervaning)
// -----------------------------------------------------------------------------
// Calculate shortest path angular difference between current heading and optimal heading
HeadingDiff := HeadingSensors.CombinedOptimalHeading - HeadingSensors.CurrentVesselHeading;

// Normalize to -180 to 180 degrees
IF HeadingDiff > 180.0 THEN
    HeadingDiff := HeadingDiff - 360.0;
ELSIF HeadingDiff < -180.0 THEN
    HeadingDiff := HeadingDiff + 360.0;
END_IF;

HeadingError := HeadingDiff;

IF EnableSystem AND NOT EmergencyShutdownSwivel THEN
    
    // Deadband to prevent continuous thruster hunting
    IF ABS(HeadingError) > HeadingDeadband THEN
        // PI Control for thruster thrust percentage
        PID_Integral := PID_Integral + (HeadingError * Ki);
        
        // Anti-windup
        IF PID_Integral > 100.0 THEN PID_Integral := 100.0; END_IF;
        IF PID_Integral < -100.0 THEN PID_Integral := -100.0; END_IF;
        
        AftThrusterCmd.ThrustSetpoint := ABS((HeadingError * Kp) + PID_Integral);
        FwdThrusterCmd.ThrustSetpoint := AftThrusterCmd.ThrustSetpoint * 0.8; // Fwd usually needs less thrust for yaw
        
        // Cap at 100%
        IF AftThrusterCmd.ThrustSetpoint > 100.0 THEN AftThrusterCmd.ThrustSetpoint := 100.0; END_IF;
        IF FwdThrusterCmd.ThrustSetpoint > 100.0 THEN FwdThrusterCmd.ThrustSetpoint := 100.0; END_IF;
        
        // Azimuth Direction (Push port or starboard based on error sign)
        IF HeadingError > 0 THEN
            // Need to turn Starboard
            AftThrusterCmd.AzimuthAngleSetpoint := 270.0; // Push to Port
            FwdThrusterCmd.AzimuthAngleSetpoint := 90.0;  // Push to Starboard
        ELSE
            // Need to turn Port
            AftThrusterCmd.AzimuthAngleSetpoint := 90.0;  // Push to Starboard
            FwdThrusterCmd.AzimuthAngleSetpoint := 270.0; // Push to Port
        END_IF;
        
        AftThrusterCmd.Enable := TRUE;
        FwdThrusterCmd.Enable := TRUE;
    ELSE
        // Within deadband
        AftThrusterCmd.ThrustSetpoint := 0.0;
        FwdThrusterCmd.ThrustSetpoint := 0.0;
        AftThrusterCmd.Enable := FALSE;
        FwdThrusterCmd.Enable := FALSE;
    END_IF;
    
ELSE
    AftThrusterCmd.Enable := FALSE;
    FwdThrusterCmd.Enable := FALSE;
    AftThrusterCmd.ThrustSetpoint := 0.0;
    FwdThrusterCmd.ThrustSetpoint := 0.0;
    PID_Integral := 0.0;
END_IF;

// Global Health
SystemHealthy := EnableSystem AND NOT EmergencyShutdownSwivel AND NOT BearingCriticalAlarm;

END_FUNCTION_BLOCK
"""

data = {
    "messages": [
        {"role": "user", "content": user_prompt},
        {"role": "assistant", "content": assistant_response}
    ]
}

with open('synthetic_generation_v3_enterprise.jsonl', 'a', encoding='utf-8') as f:
    f.write(json.dumps(data) + '\n')
